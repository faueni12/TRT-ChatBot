""" Configurações e constantes do projeto """
# -*- coding: UTF-8 -*- 
from nltk.corpus import stopwords

# Lista de palavras não tão importantes pra análise
STOP_WORDS = stopwords.words('portuguese')

# Exceto essas
STOP_WORDS.remove('não')
STOP_WORDS.remove('esta')
STOP_WORDS.remove('está')
STOP_WORDS.remove('estão')

STOP_WORDS += [
    'ramal', 'nbsp', 'bom', 'dia', 'g', 'vt', 'mat', 'nº', 'pois', 'ter', 'gentileza',
    'boa', 'tarde', 'noite', 'n', 'obrigado', 'juiz', 'hoje', 'secretaria', 'dra',
    'urgencia', 'urgência', 'humberto', 'desta', 'ser', 'segue', 'gt', 'intuito', 'obs',
    'destinar', 'ronaldo', 'compor', 'após', 'segs', 'seres.', 'conforme',
    'atenciosamente', 'natal', 'equipe', 'escola', 'segundo', 'vara', 'judicial', 'dois',
    'apoio', 'encontra-se', 'seres', 'fernades/ivia', 'ivia', 'distribuição', 
    'encaminhar', 'coordenadoria', 'feita.', 'demais', 'tácio', 'usp=sharing',
    'turma', 'possível', 'urgente', 'presidência', 'usada', 'veio', 'encontra',
    'ser', 'setor', 'favor', 'varas', 'curso', 'uso', 'servidora', 'vez', 'grata', 'grato', 
    'mary','ann', 'att', 'ramal', 'cejusc', 'juíza', 'todos', 'sessão', 'felipinho', 'falar',
    'sala', 'fica', 'sozinho', 'fazer', 'sendo', 'consegue', 'vezes', 'trabalho', 'tombo',
    
    #Acesso a rede
    'sevidor', 
]
