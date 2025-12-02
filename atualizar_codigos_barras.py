import pymysql

# Configuração do banco de dados
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Senai@118',
    database='erp_db'
)

PREFIXO = "PB"  # prefixo para o código de barras

try:
    with connection.cursor() as cursor:
        # Busca todos os produtos ordenados por ID
        cursor.execute("SELECT id, nome, codigo_barras FROM produtos ORDER BY id")
        produtos = cursor.fetchall()
        
        print(f"📊 Total de produtos encontrados: {len(produtos)}")
        
        atualizados = 0
        
        for produto in produtos:
            produto_id = produto[0]
            produto_nome = produto[1]
            codigo_atual = produto[2]
            
            # Gera o código correto baseado no ID
            codigo_correto = f"{PREFIXO}{produto_id:04d}"
            
            # Se o código atual estiver vazio ou incorreto, atualiza
            if not codigo_atual or codigo_atual != codigo_correto:
                cursor.execute(
                    "UPDATE produtos SET codigo_barras = %s WHERE id = %s",
                    (codigo_correto, produto_id)
                )
                print(f"✅ Produto ID {produto_id}: '{produto_nome}'")
                print(f"   Código definido: {codigo_correto}")
                atualizados += 1
            else:
                print(f"✓ Produto ID {produto_id}: '{produto_nome}'")
                print(f"   Código já correto: {codigo_atual}")
        
        connection.commit()
        print(f"\n🎉 Concluído! {atualizados} produtos foram atualizados.")

except Exception as e:
    print(f"❌ Erro: {e}")
    connection.rollback()

finally:
    connection.close()