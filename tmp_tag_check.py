import re
p=r'c:\\Users\\Pc\\doctr\\ticketocr\\ocrapp\\templates\\ocrapp\\upload_ticket.html'
stack=[]
pat=re.compile(r"{%\s*(if|for|block|elif|else|endif|endfor|endblock)\b(.*?)%}")
for i,line in enumerate(open(p,encoding='utf-8'),start=1):
    for m in pat.finditer(line):
        tag=m.group(1)
        if tag in ('if','for','block'):
            stack.append((tag,i))
        elif tag in ('elif','else'):
            if not stack:
                print('Orphan',tag,'at',i)
            else:
                if stack[-1][0]!='if':
                    print('Unexpected',tag,'at',i,'top',stack[-1])
        elif tag in ('endif','endfor','endblock'):
            if not stack:
                print('Orphan',tag,'at',i)
            else:
                top=stack.pop()
                exp={'if':'endif','for':'endfor','block':'endblock'}[top[0]]
                if tag!=exp:
                    print('MISMATCH closing',tag,'for',top,'at',i)

if stack:
    print('Unclosed at end:')
    for t in stack:
        print(t)
else:
    print('All balanced')
