# 📦 Guia de Upload em Lote de Imagens Faciais

## Visão Geral

O sistema agora suporta upload em lote de imagens faciais de múltiplos alunos através de um arquivo ZIP, permitindo treinar o modelo de reconhecimento facial de forma massiva e eficiente.

## 🎯 Funcionalidades

### 1. Upload em Lote
- Upload de arquivo ZIP contendo pastas com fotos de múltiplos alunos
- Processamento automático e treinamento em massa
- Validação de nomes e correspondência com alunos cadastrados
- Relatório detalhado de sucesso/falha por aluno

### 2. Exportação de Modelo
- Download do modelo treinado em formato `.pkl`
- Backup automático antes de importação
- Informações de timestamp e versão

### 3. Importação de Modelo
- Upload de modelo previamente exportado
- Validação de integridade do arquivo
- Reutilização sem necessidade de retreinamento

## 📁 Estrutura do ZIP

### Formato Requerido

```
faces.zip
├── João Silva/
│   ├── foto1.jpg
│   ├── foto2.jpg
│   ├── foto3.jpg
│   └── ...
├── Maria Santos/
│   ├── foto1.jpg
│   ├── foto2.jpg
│   └── ...
├── Pedro Oliveira/
│   ├── foto1.jpg
│   └── ...
└── ...
```

### Regras Importantes

1. **Nome das Pastas**: O nome de cada pasta DEVE corresponder **EXATAMENTE** ao nome completo do aluno cadastrado no sistema
   - ✅ Correto: `João Silva` (se cadastrado como "João Silva")
   - ❌ Incorreto: `Joao Silva`, `JOÃO SILVA`, `João` (variações não serão reconhecidas)

2. **Formatos de Imagem**: JPG, JPEG, PNG

3. **Quantidade Recomendada**: 10-30 fotos por aluno para melhor precisão

4. **Qualidade das Fotos**:
   - Boa iluminação
   - Rosto bem visível e centralizado
   - Diferentes ângulos e expressões
   - Evitar fotos muito escuras ou borradas

## 🚀 Como Usar

### Passo 1: Preparar as Imagens

1. Crie uma pasta para cada aluno com o nome completo exato
2. Adicione 10-30 fotos de boa qualidade em cada pasta
3. Compacte todas as pastas em um arquivo ZIP

### Passo 2: Verificar Nomes dos Alunos

1. Acesse o menu **"📦🖼️ Upload em Lote de Faces"**
2. Expanda **"Ver lista de nomes de alunos"** para ver os nomes exatos cadastrados
3. Certifique-se de que os nomes das pastas no ZIP correspondem exatamente

### Passo 3: Fazer Upload

1. Clique em **"Selecione o arquivo ZIP com as imagens"**
2. Escolha seu arquivo ZIP
3. Clique em **"🚀 Processar e Treinar Modelo"**
4. Revise o resumo de alunos encontrados
5. Clique em **"✅ Confirmar e Iniciar Treinamento"**

### Passo 4: Aguardar Processamento

- O sistema irá processar cada aluno sequencialmente
- Você verá o progresso em tempo real
- Ao final, um resumo será exibido com sucessos e falhas

## 💾 Gerenciamento de Modelo

### Exportar Modelo Treinado

**Quando usar:**
- Após treinar um modelo com bons resultados
- Para backup do modelo atual
- Para usar em outra instalação do sistema

**Como fazer:**
1. Acesse a aba **"💾 Gerenciar Modelo"**
2. Clique em **"📥 Baixar Modelo Treinado"**
3. Clique em **"💾 Download do Modelo"**
4. Salve o arquivo `.pkl` em local seguro

### Importar Modelo Treinado

**Quando usar:**
- Para restaurar um modelo previamente exportado
- Para evitar retreinamento após reinstalação
- Para usar modelo treinado em outra instância

**Como fazer:**
1. Acesse a aba **"💾 Gerenciar Modelo"**
2. Clique em **"Selecione o arquivo do modelo (.pkl)"**
3. Escolha o arquivo `.pkl` exportado anteriormente
4. Revise as informações do modelo
5. Clique em **"⚠️ CONFIRMAR: Substituir modelo atual"**

**⚠️ Atenção**: Importar um modelo substitui o modelo atual. Um backup automático é criado antes da substituição.

## 📊 Monitoramento

### Aba "Status do Sistema"

Visualize informações detalhadas sobre o modelo:

- **Número de alunos treinados**
- **Total de encodings gerados**
- **Média de encodings por aluno**
- **Status individual de cada aluno** (Bom, Melhorar, Insuficiente)
- **Recomendações de qualidade**

### Interpretação de Status

- ✅ **Bom**: 20+ encodings (excelente precisão)
- ⚠️ **Melhorar**: 10-19 encodings (precisão aceitável)
- ❌ **Insuficiente**: <10 encodings (considere adicionar mais fotos)

## 🎯 Melhores Práticas

### Captura de Fotos

1. **Iluminação**: Use luz natural ou iluminação uniforme
2. **Ângulos**: Capture frontal, levemente virado (esquerda/direita), acima/abaixo
3. **Expressões**: Inclua neutro, sorrindo, sério
4. **Distância**: Rosto ocupando 20-40% da altura da imagem
5. **Fundo**: Preferencialmente neutro e não distrativo

### Organização

1. Tire todas as fotos em uma sessão para consistência
2. Revise as fotos antes de adicionar ao ZIP
3. Exclua fotos borradas ou com baixa qualidade
4. Mantenha backup do ZIP original

### Manutenção do Modelo

1. **Exporte o modelo regularmente** (backup)
2. Monitore o status na aba de Status do Sistema
3. Re-treine alunos com encodings insuficientes
4. Teste o reconhecimento após treinamento em massa

## 🔧 Solução de Problemas

### Aluno não reconhecido no ZIP

**Problema**: Pasta do aluno aparece como "não reconhecida"

**Soluções**:
1. Verifique se o nome da pasta é EXATAMENTE igual ao cadastrado
2. Confira espaços extras, acentuação, maiúsculas/minúsculas
3. Consulte a lista de nomes cadastrados no sistema

### Falha no treinamento

**Problema**: Aluno aparece como "falha" após processamento

**Possíveis causas**:
1. Fotos de baixa qualidade ou sem face detectável
2. Iluminação inconsistente entre as fotos
3. Poucas fotos fornecidas

**Soluções**:
1. Verifique a qualidade das fotos manualmente
2. Tire novas fotos com melhor iluminação
3. Tente novamente com pelo menos 10-15 fotos

### Modelo não carrega após importação

**Problema**: Erro ao importar modelo

**Soluções**:
1. Verifique se o arquivo não está corrompido
2. Certifique-se de que é um arquivo `.pkl` exportado pelo sistema
3. Tente exportar o modelo atual antes de importar outro

## 📝 Exemplos de Uso

### Exemplo 1: Início do Ano Letivo

```
Cenário: Escola com 150 alunos novos

1. Cadastrar todos os 150 alunos no sistema (Cadastro Geral)
2. Tirar fotos de cada aluno (15-20 fotos por aluno)
3. Organizar em pastas com nomes dos alunos
4. Criar ZIP e fazer upload
5. Aguardar treinamento (pode levar 20-30 minutos)
6. Exportar modelo treinado para backup
7. Sistema pronto para marcar presença automaticamente
```

### Exemplo 2: Transferência entre Unidades

```
Cenário: Alunos transferidos de outra unidade que já possui modelo treinado

1. Receber arquivo .pkl do modelo da unidade origem
2. Cadastrar alunos no sistema local
3. Importar modelo .pkl
4. Sistema pronto sem necessidade de retreinamento
```

### Exemplo 3: Atualização Gradual

```
Cenário: Adicionar novos alunos ao longo do ano

Opção A - Individual:
1. Usar "Registro de Presença" para cada novo aluno
2. Captura automática de 30 fotos

Opção B - Lote mensal:
1. Acumular fotos de novos alunos do mês
2. Criar ZIP apenas com novos alunos
3. Upload em lote no final do mês
4. Exportar modelo atualizado
```

## 🔐 Segurança e Privacidade

- **Armazenamento Local**: Todos os dados são armazenados localmente
- **Formato Pickle**: Arquivos `.pkl` são binários e não facilmente legíveis
  - ⚠️ **IMPORTANTE**: Apenas importe arquivos `.pkl` de fontes confiáveis
  - Arquivos pickle podem conter código malicioso se vierem de fontes não confiáveis
  - Use apenas modelos exportados pelo próprio sistema ou de fontes verificadas
- **Backup Automático**: Sistema cria backup antes de importar novos modelos
- **Validação de ZIP**: Sistema valida caminhos de arquivo para prevenir ataques de directory traversal
- **LGPD**: Certifique-se de ter consentimento para armazenar dados biométricos

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte este guia completo
2. Verifique a aba "Status do Sistema" para diagnóstico
3. Revise os logs de erro exibidos na interface
4. Entre em contato com o suporte técnico se necessário

---

**Versão**: 1.0  
**Última atualização**: 2025-12-19
