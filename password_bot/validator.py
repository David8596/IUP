def check_pass(paswd):
    score = 0
    text = []
    
    if len(paswd) >= 8:
        score += 1
    else:
        text.append("увеличь длину до 8+")
    
    if any(c.isdigit() for c in paswd):
        score += 1
    else:
        text.append("добавь цифры")
    
    if any(c.isupper() for c in paswd):
        score += 1
    else:
        text.append("добавь заглавные буквы")
    
    if any(c in "!@#$%^&*()" for c in paswd):
        score += 1
    else:
        text.append("добавь спецсимволы")
    
    if len(paswd) >= 12:
        score += 1
    
    msg = ", ".join(text) if text else "всё ок"
    return score, msg
