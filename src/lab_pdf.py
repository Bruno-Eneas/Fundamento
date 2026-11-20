"""Leitor experimental de PDF textual de exames *fictícios e anonimizados*.

Extrai valores apenas com rótulos explícitos e unidades corretas. Nenhuma inferência
ocorre até revisão manual; documentos escaneados/ambíguos não são interpretados.
"""
import io
import re
from pypdf import PdfReader

LIMIT_BYTES=5*1024*1024
LABELS={
 "glicemia_jejum": re.compile(r"(?:glicemia|glicose)(?:\s+plasm[aá]tica)?\s+(?:em\s+)?jejum",re.I),
 "hba1c": re.compile(r"(?:hemoglobina\s+glicada|hba1c|a1c\s*\(?%)",re.I),
 "ttgo_1h": re.compile(r"(?:ttgo|t[oô]ler[aâ]ncia\s+[aà]\s+glicose)[^\n]{0,20}(?:1\s*h(?:ora)?|60\s*min)",re.I),
 "ttgo_2h": re.compile(r"(?:ttgo|t[oô]ler[aâ]ncia\s+[aà]\s+glicose)[^\n]{0,20}(?:2\s*h(?:oras)?|120\s*min)",re.I),
}
VALUE=re.compile(r"(?<!\d)(\d{1,3}(?:[.,]\d{1,2})?)\s*(mg\s*/\s*d[lL]|%)",re.I)


def extract_labs_from_pdf(data:bytes):
    if not data or len(data)>LIMIT_BYTES or not data.startswith(b'%PDF'):
        raise ValueError('Envie um PDF de até 5 MB e com conteúdo válido.')
    try:
        r=PdfReader(io.BytesIO(data),strict=True)
        if r.is_encrypted:
            raise ValueError('PDF com senha: não é possível analisar.')
        if len(r.pages)>8:
            raise ValueError('O demonstrativo aceita no máximo 8 páginas.')
        pages=[p.extract_text(extraction_mode='plain') or '' for p in r.pages]
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError('Não foi possível ler o texto do PDF. Use entrada manual.') from exc
    text='\n'.join(pages)
    if not text.strip():
        return {}, ['Arquivo sem texto selecionável (ex.: imagem escaneada). Digite os valores manualmente.']
    found={}
    blocked=set()
    notices=[]
    for line in text.splitlines():
        line=' '.join(line.strip().split())
        if not line:
            continue
        for key,pattern in LABELS.items():
            match=pattern.search(line)
            if not match or key in blocked:
                continue
            # Só o trecho depois do rótulo é procurado; não capturar referência anterior.
            after=line[match.end():match.end()+65]
            vmatch=VALUE.search(after)
            if not vmatch:
                continue
            unit=vmatch.group(2).lower().replace(' ','')
            expected='%' if key=='hba1c' else 'mg/dl'
            if unit!=expected:
                continue
            value=float(vmatch.group(1).replace(',','.'))
            if key in found and found[key]!=value:
                notices.append('Valores repetidos e diferentes para '+key+'; verifique manualmente.')
                found.pop(key,None)
                blocked.add(key)
                continue
            found[key]=value
    if not found:
        notices.append('Não foram encontrados rótulos e unidades inequívocos. Informe os resultados manualmente.')
    notices.append('Os valores extraídos são rascunhos: confira rótulo, data, amostra, unidade e condição de coleta no PDF original.')
    return found, notices
