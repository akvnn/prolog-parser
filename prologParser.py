#%% Lexical Analyzer
from enum import Enum #, auto

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
outputFile = 'parser_output.txt'
lexeme = []
lexLen = 0

nextCharacter = ''
nextToken = None
charClass = None

lineNumber = 1
charNumber = 0
errorCount = 0
lines = []
#%%
def parser_out(message, error = True):
    global errorCount
    if error: 
        errorCount += 1
        with open(outputFile, 'a') as file:
            file.write(f'{message} on line {lineNumber}, character {charNumber}\n')
    else:
        with open(outputFile, 'a') as file:
            file.write(f'{message}\n')
    
#%% Lexical Analyzer Functions
def run():
    global fileString, fileStringIterator, nextToken, errorCount, lineNumber, charNumber, lines  
    try: 
        with open(outputFile, 'w') as file: # clear output file
            file.write('')  
        fileIndex = 1
        while True:
            with open(f'{fileIndex}.txt', 'r') as file:
            
                fileString = file.read()
                lines = fileString.split('\n')
                fileStringIterator = iter(fileString)
                lineNumber = 1
                charNumber = 0
                errorCount = 0
                getChar()
                lex()
                print(f'Parsing file {fileIndex}...')
                parser_out(f'Parsing file {fileIndex}...', error = False)
                program()
                print(f'Parsing file {fileIndex} complete! {errorCount} errors were found') 
                parser_out(f'Parsing file {fileIndex} complete! {errorCount} error{" was" if errorCount == 1 else "s were"} found', error=False)
                fileIndex += 1
            # while nextToken != TokenCodes.EOF: 
            #     lex()
    except FileNotFoundError:
        print(f"Parsed all {fileIndex - 1} files!")
        parser_out(f"Parsed all {fileIndex - 1} files!", error = False)
    except Exception as error:
        print(f'An error occurred: {error}')

def addChar():
    global lexLen, nextCharacter, lexeme
    
    if lexLen <= 98:
        lexLen += 1
        lexeme.append(nextCharacter)
    else: 
        print("Lexeme exceeded 98 characters!")

def getChar():
    global nextCharacter, fileStringIterator, charClass, charNumber, lineNumber

    try: 
        nextCharacter = next(fileStringIterator)
        
        if nextCharacter.isalpha() or nextCharacter == '_':
            charClass = CharacterClasses.LETTER
        elif nextCharacter.isnumeric():
            charClass = CharacterClasses.DIGIT
        else: 
            charClass = CharacterClasses.UNKNOWN
        
        if not nextCharacter == '\n':
            charNumber += 1
        else: 
            lineNumber += 1
            charNumber = 0
            
    except StopIteration:
        charClass = CharacterClasses.EOF

def lex(): 
    global nextCharacter, charClass, nextToken, lexeme, lexLen
    
    lexeme = []
    lexLen = 0
    
    while nextCharacter == ' ' or nextCharacter == '\n':
        getChar()
    
    # Parse identifiers
    if charClass == CharacterClasses.LETTER: 
        addChar()
        getChar()
        while charClass == CharacterClasses.LETTER or charClass == CharacterClasses.DIGIT:
            addChar()
            getChar()
        nextToken = TokenCodes.IDENT
    
    # Parse integer literals
    elif charClass == CharacterClasses.DIGIT:
        addChar()
        getChar()
        while charClass == CharacterClasses.DIGIT:
            addChar()
            getChar()
        nextToken = TokenCodes.INT_LIT
    
    # Paranthesis and Operators
    elif charClass == CharacterClasses.UNKNOWN:
        if nextCharacter == '?' or nextCharacter == ':':
            
            # Consider the character that follows it directly, if its '-', then we have a 
            # special operator
            former = nextCharacter # Store the former
            addChar()
            getChar() # Check the next character
            
            if nextCharacter == '-':
                # Special case
                nextToken = lookup(former + nextCharacter) # addChar() is called within
                # getChar() # go to the next character
            else: 
                nextToken = lookup(former)
        else:
            nextToken = lookup(nextCharacter)
            # getChar()
        # No need to call it here (we're calling it above anyways)
        getChar()
    
    # End Of File
    elif charClass == CharacterClasses.EOF:
        nextToken = TokenCodes.EOF
        lexeme = ['E', 'O', 'F', 0]

    print(f"Next token is {nextToken}, Next lexeme is: {lexeme}")
    
    return nextToken

def lookup(character): 
    characterToken = None
    
    try:
        characterToken = lookupDictionary[character]
    except KeyError: 
        # Error: Symbol Not Recognized?
        print(f'Symbol {character} is not recognized in the grammar of the language')
        parser_out(f"SyntaxError symbol {character} is not recognized")
        characterToken = TokenCodes.EOF # To Do

    addChar()
    return characterToken
#%% Syntax Analyzer
def program():
    print("Enter <program>")
    if nextToken == TokenCodes.QUERY_OPERATOR :
        query()
    else:
        clause_list()
        # lex() 
        query()
    if nextToken != TokenCodes.EOF:
        print("\033[91mError: Missing EOF\033[0m")
        parser_out(f"SyntaxError expected EOF but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
        # continue parsing
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
            parser_out(f"SyntaxError expcted '.' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
            # continue parsing
            
    else:
        print("\033[91mError: Missing query operator\033[0m")
        parser_out(f"SyntaxError expected '?-' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
        # continue parsing
    print("Exit <query>")
    
def clause_list(optional = False):
    print("Enter <clause_list>")
    if optional == True:
        error = clause(optional)
        if error == True:
            return    
    else:
        clause()    
    # lex() 
    clause_list(optional = True)
    print("Exit <clause_list>")
    
def clause(optional = False):
    print("Enter <clause>")
    predicate(optional)
    # lex() # commented lex() here
    if nextToken == TokenCodes.DEFINITION_OPERATOR:
        lex()
        predicate_list()
    elif nextToken != TokenCodes.DOT:
        if optional == True:
            return True
        print("\033[91mError: Clause missing period\033[0m")
        parser_out(f"SyntaxError expcted '.' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]}instead")
        # continue parsing
        
    lex() # match the period
    print("Exit <clause>")
    
def predicate_list(optional = False):
    print("Enter <predicate_list>")
    predicate()
    # lex() # commented lex() here
    if nextToken == TokenCodes.COMMA:
        lex()
        predicate_list()
    print("Exit <predicate_list>")
    
def predicate(optional = False):
    print("Enter <predicate>")
    atom(optional)
    # lex() 
    if(nextToken == TokenCodes.LEFT_PAREN):
        lex()
        term_list()
        if(nextToken == TokenCodes.RIGHT_PAREN):
            lex()
        else:
            if optional == True:
                return True
            print("\033[91mError: Missing right parenthesis in predicate\033[0m")
            parser_out(f"SyntaxError expcted ')' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
            # continue parsing
    print("Exit <predicate>")
    
def term_list(optional = False):
    print("Enter <term_list>")
    term()
    if(nextToken == TokenCodes.COMMA):
        lex()
        term_list()
    print("Exit <term_list>")
    
def term(optional = False):
    print("Enter <term>")
    # can be atom or variable or structure or numeral
    if nextToken == TokenCodes.IDENT or (len(lexeme) > 0 and lexeme[0] == '_'): 
        if len(lexeme) > 0 and (lexeme[0].isupper() or lexeme[0] == '_'):
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
                    parser_out(f"SyntaxError expcted ')' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
                    # continue parsing
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
            parser_out(f"SyntaxError expcted ''' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
            # continue parsing
    else:
        if optional == True:
            return True
        print(nextToken, ' in atom')
        print("\033[91mError: Missing atom\033[0m")
        parser_out(f"SyntaxError expected a lowercase character or ''' but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
        # continue parsing
    print("Exit <atom>")
    
def small_atom(optional = False):
    print("Enter <small_atom>")
    lowercase_char(optional)
    lex()
    character_list(optional = True)
    
    print("Exit <small_atom>")
    
def lowercase_char(optional = False):
    print("Enter <lowercase_char>")
    if len(lexeme) > 0 and lexeme[0].islower():
        lexeme.pop(0)
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing lowercase character \033[0m")
        parser_out(f"SyntaxError expected a lowercase character but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
    print("Exit <lowercase_char>")
    
def uppercase_char(optional = False):
    print("Enter <uppercase_char>")
    if len(lexeme) > 0 and (lexeme[0].isupper() or lexeme[0] == '_'):
        lexeme.pop(0)
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing uppercase character\033[0m")
        parser_out(f"SyntaxError expected an uppercase character but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
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
    if len(lexeme) > 0:
        if lexeme[0].islower():
            lowercase_char(optional)
        elif lexeme[0].isnumeric():
            digit(optional)
        elif lexeme[0].isupper():
            uppercase_char(optional)
        else:
            if optional == True:
                return True
            print("\033[91mError: Missing alphanumeric character\033[0m")
            parser_out(f"SyntaxError expected an alphanumeric character but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
            
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing alphanumeric character\033[0m")
        parser_out(f"SyntaxError expected an alphanumeric character but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
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
    if len(lexeme) > 0 and lexeme[0].isdigit():
        lexeme.pop(0)
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing digit\033[0m")
        parser_out(f"SyntaxError expected a digit but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
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
            parser_out(f"SyntaxError expected a character but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead")
    print("Exit <character>")
    
def special(optional = False):
    print("Enter <special>")
    if len(lexeme > 0) and lexeme[0] in ['+', '-', '*', '/', '\\', '^', '~', ':', '.', '?', '#', '$', '&']:
        lexeme.pop(0)
    else:
        if optional == True:
            return True
        print("\033[91mError: Missing special character\033[0m")
        parser_out(f"SyntaxError expected a special character (+ | - | * | / | \ | ^ | ~ | : | . | ? | # | $ | & ) but found {lexeme[0] if len(lexeme) > 0 else 'line ' + lines[lineNumber - 1]} instead") 
    print("Exit <special>")
    
def variable(optional = False):
    print("Enter <variable>")
    upperCaseError = uppercase_char(optional)
    if upperCaseError == True:
        return True
    lex() 
    character_list(optional = True)
    print("Exit <variable>")
   
        
    
#%% Driver
run()
# %%
