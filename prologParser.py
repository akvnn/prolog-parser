#%% Tokens and Character Classes
from enum import Enum, auto

class CharacterClasses(Enum):
    LETTER = 0
    DIGIT = 1
    UNKNOWN = 99
    EOF = 100

class TokenCodes(Enum):
    INT_LIT = 10
    IDENT = 11
    ASSIGN_OP = 20
    LEFT_PAREN = 25
    RIGHT_PAREN = 26
    ADD_OP = 21
    SUB_OP = 22
    MULT_OP = 23
    DIV_OP = 24
    CARROT = 27
    COLON = 28
    DOT = 29
    QUESTION_MARK = 30
    UNDERSCORE = 31
    HASH_SYMBOL = 32
    DOLLAR_SIGN = 33
    AND_OP = 34
    COMMA = 35
    DEFINITION_OPERATOR = 36
    QUERY_OPERATOR = 37
    WAVE_SIGN = 38
    BACKSLASH = 39
    SINGLE_QUOTE = 40
    EOF = 50

lookupDictionary = {
    '(': TokenCodes.LEFT_PAREN,
    ')': TokenCodes.RIGHT_PAREN,
    '+': TokenCodes.ADD_OP,
    '-': TokenCodes.SUB_OP,
    '*': TokenCodes.MULT_OP,
    '/': TokenCodes.DIV_OP,
    '^': TokenCodes.CARROT,
    ':': TokenCodes.COLON,
    '?': TokenCodes.QUESTION_MARK,
    '_': TokenCodes.UNDERSCORE,
    '#': TokenCodes.HASH_SYMBOL,
    '$': TokenCodes.DOLLAR_SIGN,
    '&': TokenCodes.AND_OP,
    '.': TokenCodes.DOT,
    ',': TokenCodes.COMMA, 
    ':-': TokenCodes.DEFINITION_OPERATOR,
    '?-': TokenCodes.QUERY_OPERATOR,
    '~': TokenCodes.WAVE_SIGN,
    '\\': TokenCodes.BACKSLASH,
    "'": TokenCodes.SINGLE_QUOTE   
}


#%% Globals
fileString = ''
fileStringIterator = None

lexeme = []
lexLen = 0

nextCharacter = ''
nextToken = None
charClass = None

#%% Lexical Analyzer Functions
def run(filePathString):
    try: 
        with open(filePathString, 'r') as file:
            global fileString
            global fileStringIterator
            global nextToken
            
            fileString = file.read()
            fileStringIterator = iter(fileString)
                        
            getChar()
            lex()
            program()
            # while nextToken != TokenCodes.EOF: 
            #     lex()
    except FileNotFoundError:
        print(f"The file '{filePathString}' was not found")
    except Exception as error:
        print(f'An error occurred: {error}')

def addChar():
    global lexLen
    global nextCharacter
    global lexeme
    
    if lexLen <= 98:
        lexLen += 1
        lexeme.append(nextCharacter)
    else: 
        print("Lexeme exceeded 98 characters!")

def getChar():
    global nextCharacter
    global fileStringIterator
    global charClass

    try: 
        nextCharacter = next(fileStringIterator)
        
        if nextCharacter.isalpha():
            charClass = CharacterClasses.LETTER
        elif nextCharacter.isnumeric():
            charClass = CharacterClasses.DIGIT
        else: 
            charClass = CharacterClasses.UNKNOWN
    except StopIteration:
        charClass = CharacterClasses.EOF

def lex(): 
    global nextCharacter
    global charClass
    global nextToken
    global lexeme
    global lexLen
    

    
    lexeme = []
    lexLen = 0
    
    while nextCharacter == ' ' or nextCharacter == '\n':
        getChar()
    
    # Parse identifiers
    if charClass == CharacterClasses.LETTER: 
        addChar()
        getChar()
        # while charClass == CharacterClasses.LETTER or charClass == CharacterClasses.DIGIT:
        #     addChar()
        #     getChar()
        nextToken = TokenCodes.IDENT
    
    # Parse integer literals
    elif charClass == CharacterClasses.DIGIT:
        addChar()
        getChar()
        # while charClass == CharacterClasses.DIGIT:
        #     addChar()
        #     getChar()
        nextToken = TokenCodes.INT_LIT
    
    # Paranthesis and Operators
    elif charClass == CharacterClasses.UNKNOWN:
        # Return an error? Unknown character
        nextToken = lookup(nextCharacter)
        getChar()
    
    # End Of File
    elif charClass == CharacterClasses.EOF:
        nextToken = TokenCodes.EOF
        lexeme = ['E', 'O', 'F', 0]

    print(f"Next token is {nextToken}, Next lexeme is: {lexeme}")
    # in the case of a definition operator, lexeme is [':', '-']
    
    return nextToken

def lookup(character): 
    global fileStringIterator #ak added this
    global nextCharacter #ak added this
    global lexeme #ak added this
    characterToken = None
    
    try:
        characterToken = lookupDictionary[character]
        
        if characterToken == TokenCodes.COLON or characterToken == TokenCodes.QUESTION_MARK: # ak added this
            nextCharacter = next(fileStringIterator)
            if nextCharacter == '-':
                lexeme.append(character)
                characterToken = lookupDictionary[character + nextCharacter]
            else:
                # revert back to previous character to do...
                print('reverting back to previous character')
    except KeyError: 
        # Error: Symbol Not Recognized?
        characterToken = TokenCodes.EOF

    addChar()
    return characterToken

#%%
def program():
    print("Enter <program>")
    if nextToken == TokenCodes.QUERY_OPERATOR :
        query()
    else:
        clause_list()
        lex() 
        query()
    print("Exit <program>")
    
def query():
    print("Enter <query>")
    if nextToken == TokenCodes.QUERY_OPERATOR:
        lex()
        predicate_list()
        if nextToken == TokenCodes.DOT:
            lex()
        else: 
            print("\033[91mError: Missing period\033[0m")
    else:
        print("\033[91mError: Missing query operator\033[0m")
    print("Exit <query>")
    
def clause_list(optional = False):
    print("Enter <clause_list>")
    if optional == True:
        error = clause(optional)
        if error == True:
            return    
    else:
        clause()    
    lex() 
    clause_list(optional = True)
    print("Exit <clause_list>")
def clause(optional = False):
    print("Enter <clause>")
    predicate(optional)
    # lex() # commented lex() here
    if nextToken == TokenCodes.DEFINITION_OPERATOR:
        lex()
        predicate_list(optional)
    elif nextToken != TokenCodes.DOT:
        if optional == True:
            return True
        print("\033[91mError: Clause missing period\033[0m")
    lex() # match the period
    print("Exit <clause>")
def predicate_list(optional = False):
    print("Enter <predicate_list>")
    predicate(optional)
    # lex() # added lex() here
    if nextToken == TokenCodes.COMMA:
        lex()
        predicate_list(optional)
    print("Exit <predicate_list>")
def predicate(optional = False):
    print("Enter <predicate>")
    atom(optional)
    lex() # this lex should not be here?
    if(nextToken == TokenCodes.LEFT_PAREN):
        lex()
        term_list(optional)
        if(nextToken == TokenCodes.RIGHT_PAREN):
            lex()
        else:
            if optional == True:
                return True
            print("\033[91mError: Missing right parenthesis in predicate\033[0m")
    print("Exit <predicate>")
def term_list(optional = False):
    print("Enter <term_list>")
    term(optional)
    if(nextToken == TokenCodes.COMMA):
        lex()
        term_list(optional)
    print("Exit <term_list>")
def term(optional = False):
    print("Enter <term>")
    print(nextToken, ' in term')
    # can be atom or variable or structure or numeral
    if nextToken == TokenCodes.IDENT: 
        # if nextCharacter.isupper(): # wrong ? 
        # if lexeme[0].isupper(): 
        if nextCharacter.isupper(): #not working.
            variable()
        else:
            atom()
            if nextToken == TokenCodes.LEFT_PAREN: # structure merged here
                lex()
                term_list()
                if nextToken == TokenCodes.RIGHT_PAREN:
                    lex()
                else:
                    if optional == True:
                        return True
                    print("\033[91mError: Missing right parenthesis\033[0m")
    elif nextToken==TokenCodes.INT_LIT:
        numeral()
    print("Exit <term>")
def atom(optional = False):
    print("Enter <atom>")
    if nextToken == TokenCodes.IDENT:
        small_atom(optional)
    elif nextToken == TokenCodes.SINGLE_QUOTE:
        lex()
        string()
        if nextToken == TokenCodes.SINGLE_QUOTE:
            lex()
        else:
            if optional == True:
                return True
            print("\033[91mError: Missing single quote\033[0m")
    else:
        if optional == True:
            return True
        print(nextToken, ' in atom')
        print("\033[91mError: Missing atom\033[0m")
    print("Exit <atom>")
    
def small_atom(optional = False):
    print("Enter <small_atom>")
    lowercase_char(optional)
    lex() 
    character_list(optional = True)
    
    print("Exit <small_atom>")
    
def lowercase_char(optional = False):
    print("Enter <lowercase_char>")
    # if lexeme[0].islower():
    if nextCharacter.islower():
        lex()
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing lowercase character \033[0m")
    print("Exit <lowercase_char>")
    
def uppercase_char(optional = False):
    print("Enter <uppercase_char>")
    # if nextCharacter.isupper() or nextCharacter == '_':
    if nextCharacter.isupper() or nextCharacter == '_':
        lex()
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing uppercase character\033[0m")
    print("Exit <uppercase_char>")
def character_list(optional = False):
    print("Enter <character_list>")
    anError = alphanumeric(optional)
    if anError == True:
        return True
    character_list(optional = True)
    print("Exit <character_list>")
def alphanumeric(optional = False):
    print("Enter <alphanumeric>")
    if nextCharacter.islower():
        lowercase_char(optional)
    elif nextCharacter.isnumeric():
        digit(optional)
    elif nextCharacter.isupper():
        uppercase_char(optional)
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing alphanumeric character\033[0m")
    print("Exit <alphanumeric>")

def numeral(optional = False):
    print("Enter <numeral>")
    isDigitError = digit(optional)
    if isDigitError == True:
        return True
    lex() 
    numeral(optional = True)
    print("Exit <numeral>")
def digit(optional = False):
    print("Enter <digit>")
    if nextCharacter.isnumeric():
        lex()
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing digit\033[0m")
    print("Exit <digit>")
def string(optional = False):
    print("Enter <string>")
    charError = character(optional)
    if charError == True:
        return True
    lex() 
    string(optional = True)
    print("Exit <string>")    
def character(optional = False):
    isAlphanumericError = alphanumeric(optional = True)
    if isAlphanumericError == True:
        isSpecialError = special(optional = True)
        if isSpecialError == True:
            if optional == True:
                return True
            print("\033[91mError: Missing character\033[0m")
    print("Exit <character>")
def special(optional = False):
    print("Enter <special>")
    specialChar = nextToken
    if specialChar == TokenCodes.AND_OP or specialChar == TokenCodes.QUESTION_MARK or specialChar == TokenCodes.HASH_SYMBOL or specialChar == TokenCodes.DOLLAR_SIGN or specialChar == TokenCodes.ADD_OP or specialChar == TokenCodes.SUB_OP or specialChar == TokenCodes.COLON or specialChar == TokenCodes.DOT or specialChar == TokenCodes.MULT_OP or specialChar == TokenCodes.DIV_OP or specialChar == TokenCodes.CARROT or specialChar == TokenCodes.WAVE_SIGN or specialChar == TokenCodes.BACKSLASH:
        lex()
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing special character\033[0m")
    print("Exit <special>")
def variable(optional = False):
    print("Enter <variable>")
    upperCaseError = uppercase_char(optional)
    if upperCaseError == True:
        return True
    # lex() # commented lex out for now
    character_list(optional = True)
    print("Exit <variable>")
   
        
    
#%%

run('test.txt')
#%%


# %%
