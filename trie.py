class Trie:
    '''A Trie is a prefix tree that stores words organized by their prefixes and holds a frequency variable
    that stores how many times the word appears in some source text. A trie allows you to return the most frequent
    words that start with some prefix or are one-letter edit away from the prefix. Its function is similar to
    Google's autocomplete and autocorrect dropdown lists that appear when typing in a search bar.
    '''
    def __init__(self):
        self.frequency = 0
        self.children = {}

    # add word/frequency to the trie.  Increment frequency
    # if no value supplied.
    def insert(self, word, frequency=None):
        
        if word is '':
            if frequency is None:
                self.frequency += 1
            else:
                self.frequency = frequency
        else:
            letter = word[0]
            if self.children.get(letter) is None:
                self.children[letter] = Trie()
            self.children[letter].insert(word[1:],frequency)
            
    # return trie node for specified prefix, None if not in trie
    def find(self,prefix):
        if prefix is '':
            return self
        else:
            if self.children.get(prefix[0]) is None:
                return None
            return self.children[prefix[0]].find(prefix[1:])

    # is word in trie? return True or False
    def __contains__(self, word):
        answer = self.find(word)
        if answer is None:
            return False
        else:
            if answer.frequency == 0:
                return False
            return True

    # return list of [word,freq] pairs for all words in
    # this trie and its children
    def __iter__(self):
        '''yields [word,freq] of self if self is a word. recursively calls __iter__ on the children and yields
        [new letter + their word,freq]'''
        if self.frequency > 0:
            yield ['',self.frequency]
        for letter in self.children:
            for word,freq in self.children[letter]:
                yield [letter+word,freq]
        
    
    ##################################################
    ## additional methods
    ##################################################

    # return the list of N most-frequently occurring words that start with prefix.
    def autocomplete(self, prefix, N):
        '''Finds the node with the prefix. Sorts the iterable [word,freq] list by freq of the 
        subtrie starting with that prefix. Pops off the resulting sorted list until N are reached or until
        there are no more nodes.
        '''
        prefixNode = self.find(prefix)
        if prefixNode is None:
            return []
        pairs = list(prefixNode)[:]
        pairs.sort(key=lambda tup : tup[1])
        count = 0
        mostFrequent = []
        while count < N and len(pairs) > 0:
            best = pairs.pop()
            mostFrequent.append(prefix+best[0])
            count += 1
        return mostFrequent
            
        
    # return the list of N most-frequent words that start with prefix or that
    # are valid words that differ from prefix by a small edit
    def autocorrect(self, prefix, N):
        '''First computes all four types of the valid one-letter edits that are also 
        valid words in the trie. Then loops through the trie to obtain the word,freq lists of the valid edits 
        in the trie. It sorts the resulting valid nodes by frequency and pops off the top 
        until the required number of nodes are appended'''
        mostFrequent = self.autocomplete(prefix,N)
        if len(mostFrequent) == N:
            return mostFrequent
        numNeeded = N-len(mostFrequent)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        validEdits = []
        allNodes = list(self)
        validWords = []
        for word,freq in allNodes:
            if freq > 0:
                validWords.append(word)
                
        for index in range(len(prefix)+1):
            for letter in alphabet:
                insertionEdit = prefix[0:index] + letter + prefix[index:]
                if insertionEdit in validWords:
                    validEdits.append(insertionEdit)
                if index < len(prefix):
                    replaceEdit = prefix[0:index] + letter + prefix[index+1:]
                    if replaceEdit in validWords:
                        validEdits.append(replaceEdit)
            if index < len(prefix):
                deletionEdit = prefix[0:index] + prefix[index+1:]
                if deletionEdit in validWords:
                    validEdits.append(deletionEdit)
            if index < len(prefix)-1:
                transposeEdit = prefix[0:index] + prefix[index+1] + prefix[index] + prefix[index+2:]
                if transposeEdit in validWords:
                    validEdits.append(transposeEdit)
        
        validNodes = []
        for word,freq in self:
            if word is not prefix and word in validEdits:
                validNodes.append([word,freq])
        validNodes.sort(key=lambda tup: tup[1])
        
        
        count = 0
        while count < numNeeded and len(validNodes) > 0:
            best = validNodes.pop()
            if best[0] not in mostFrequent:
                mostFrequent.append(best[0])
            count += 1
        
        return mostFrequent
            

    # return list of [word, freq] for all words in trie that match pattern
    # pattern is a string, interpreted as explained below
    #   * matches any sequence of zero or more characters
    #   ? matches any single character
    #   otherwise char in pattern char must equal char in word
    def filter(self,pattern):
        '''Loops through the trie and tries to match every word with the pattern.'''
        answer = []
        for word,freq in self:
            if self.match(pattern,word):
                answer.append([word,freq])
        return answer
    def match(self,remainingPattern,remainingWord):
        '''Checks the next letter of the remainingPattern and sees if it matches any of the beginning
        of remainingWord. Recursively checks remainingPattern[1:] and remainingWord[endIndex:] and returns
        the result of match called upon those two'''
    
        if remainingPattern is '':
            if remainingWord is '':
                return True
            return False
        elif remainingWord is '':
            for letter in remainingPattern:
                if letter is not '*':
                    return False
            return True
        
        nextChar = remainingPattern[0]
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        if nextChar in alphabet:
            if remainingWord[0] is nextChar:
                return self.match(remainingPattern[1:],remainingWord[1:])
            else:
                return False
        elif nextChar is '*':
            for endIndex in range(len(remainingWord)+1):
                if self.match(remainingPattern[1:],remainingWord[endIndex:]) is True:
                    return True
            return False
        elif nextChar is '?':
            if remainingWord is '':
                return False
            return self.match(remainingPattern[1:],remainingWord[1:])
