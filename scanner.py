codeToBeScanned = """
int main() {
    int x,y;
    // This is a single-line comment
    if (x == 42) {
        /* This is
           a block
           comment */
        x = x-3;
    } else {
        y = 3.1; // Another comment
    }
    return 0;
}
"""

def scanner(code):
  #handle comments
  comments = []
  filteredCode = ""
  insideBlock = False
  blockComment = ""

  for line in code.split("\n"):
      if insideBlock:
          if "*/" in line:
            #  part_after_end for cases like x; /*random thing*/ y; 
              part_before_end, part_after_end = line.split("*/", 1)
              blockComment += part_before_end
              comments.append(blockComment.strip())
              #reset the block comment accumelator 
              blockComment = ""
              insideBlock = False
              filteredCode += part_after_end + "\n"
          else:
              blockComment += line + "\n"
          continue
      if "//" in line:
          code_part, comment_part = line.split("//", 1)
          filteredCode += code_part + "\n"
          comments.append(comment_part.strip())
      elif "/*" in line:
          part_before, part_after = line.split("/*", 1)
          filteredCode += part_before
          if "*/" in part_after:
              comment_part, rest = part_after.split("*/", 1)
              comments.append(comment_part.strip())
              filteredCode += rest + "\n"
          else:
              blockComment = part_after + "\n"
              insideBlock = True
              filteredCode += "\n"
      
      else:
          filteredCode += line + "\n"
  print("------")
  print(comments)
  print("------")
  #tokens
  keywords = ["int", "float", "char", "if", "else", "for", "while", "return"]
  special_chars = ["(", ")", "{", "}", "[", "]", ";", ","]
  operators = ["+", "-", "*", "/", "="]

  tokens = []
  current_token = ""
  for char in filteredCode:
      #when spacing or starting a new line we check the token we built
      if char == " " or char == "\n":
          if current_token != "":
              if current_token in keywords:
                  tokens.append(("Keyword", current_token))
              #handle floats
              elif current_token.replace(".", "").isdigit():
                  tokens.append(("Constant", current_token))
              #if not a number or a keyword, then it's an identifier
              else:
                  tokens.append(("Identifier", current_token))
              #reset
              current_token = ""
      elif char in special_chars or char in operators:
          #save any token we were building first then add the special char or operator
          if current_token != "":
              if current_token in keywords:
                  tokens.append(("Keyword", current_token))
              elif current_token.replace(".", "").isdigit():
                  tokens.append(("Constant", current_token))
              else:
                  tokens.append(("Identifier", current_token))
              current_token = ""
          
          # add the special char or operator
          if char in special_chars:
              tokens.append(("Special Character", char))
          elif char in operators:
              tokens.append(("Operator", char))
      else:
          current_token += char

  if current_token != "":
      if current_token in keywords:
          tokens.append(("Keyword", current_token))
      elif current_token.replace(".", "").isdigit():
          tokens.append(("Constant", current_token))
      else:
          tokens.append(("Identifier", current_token))

  print(tokens)

scanner(codeToBeScanned)