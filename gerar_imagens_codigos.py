import os
import barcode
from barcode.writer import ImageWriter
import pymysql

# Configuração do banco de dados
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Senai@118',
    database='erp_db'
)

# Pasta para salvar as imagens
PASTA_BARCODES = "static/barcodes"
os.makedirs(PASTA_BARCODES, exist_ok=True)

try:
    with connection.cursor() as cursor:
        # Busca todos os produtos com códigos de barras
        cursor.execute("SELECT id, nome, codigo_barras FROM produtos WHERE codigo_barras IS NOT NULL AND codigo_barras != ''")
        produtos = cursor.fetchall()
        
        print(f"📊 Produtos encontrados: {len(produtos)}")
        
        if len(produtos) == 0:
            print("⚠️ Nenhum produto com código de barras encontrado!")
            print("Execute primeiro: python atualizar_codigos_barras.py")
        
        for produto in produtos:
            produto_id = produto[0]
            produto_nome = produto[1]
            codigo_barras = produto[2]
            
            # Gera código de barras Code 128
            try:
                barcode_class = barcode.get_barcode_class('code128')
                codigo_barra = barcode_class(codigo_barras, writer=ImageWriter())
                
                caminho_arquivo = os.path.join(PASTA_BARCODES, f"{codigo_barras}.png")
                codigo_barra.save(caminho_arquivo)
                print(f"✅ Imagem gerada para '{produto_nome}'")
                print(f"   ID: {produto_id} | Código: {codigo_barras}")
            except Exception as e:
                print(f"❌ Erro ao gerar código para '{produto_nome}': {e}")

    print(f"\n🎉 Todas as imagens foram geradas em '{PASTA_BARCODES}/'")

except Exception as e:
    print(f"❌ Erro: {e}")

finally:
    connection.close()

# Verifica as imagens geradas
print(f"\n📁 Conteúdo da pasta '{PASTA_BARCODES}':")
if os.path.exists(PASTA_BARCODES):
    arquivos = os.listdir(PASTA_BARCODES)
    if arquivos:
        for arquivo in sorted(arquivos):
            if arquivo.endswith('.png'):
                tamanho = os.path.getsize(os.path.join(PASTA_BARCODES, arquivo))
                print(f"  • {arquivo} ({tamanho} bytes)")
    else:
        print("  (pasta vazia)")
else:
    print("  (pasta não existe)")