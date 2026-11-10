import re

with open('solution/latex/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Add \usepackage{amssymb}
text = text.replace(r'\usepackage{eurosym}', r'\usepackage{eurosym}' + '\n' + r'\usepackage{amssymb}')

# Replace \varnothing with \diameter or \Phi or Ø
text = text.replace(r'$\varnothing$', r'Ø')

# Fix footskip
text = text.replace(r'footskip=12pt', r'footskip=14pt')

# In page 4, the two minipages at lines 310-380:
# \begin{minipage}[t]{0.485\textwidth} ... \end{minipage}\hfill\begin{minipage}[t]{0.485\textwidth}
# Let's inspect the tables inside:
# Table A5 has 4 columns: {l c l r} which might overflow if total width is fixed or not wrapped.
# Let's use tabularx with {l c X r}!
text = text.replace(r'\begin{tabularx}{\textwidth}{l c l r}', r'\begin{tabularx}{\textwidth}{l c X r}')

with open('solution/latex/main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated main.tex")
