import type { NextApiRequest, NextApiResponse } from 'next'
import { ChatOpenAI } from 'langchain/chat_models/openai'
import { OpenAIEmbeddings } from 'langchain/embeddings/openai'
import { FAISS } from 'langchain/vectorstores/faiss'

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  const { query } = req.body
  if (!query || typeof query !== 'string') return res.status(400).json({ error: 'Invalid query input' })

  try {
    const embeddings = new OpenAIEmbeddings()
    const vectorstore = await FAISS.loadLocal('./faiss_index', embeddings)
    const docs = await vectorstore.similaritySearch(query, 3)
    const context = docs.map(doc => doc.pageContent).join('\n')

    const llm = new ChatOpenAI({ modelName: 'gpt-4' })
    const prompt = `Use the context below to answer the question.\n\nContext:\n${context}\n\nQuestion: ${query}\nAnswer:`
    const response = await llm.predict(prompt)

    return res.status(200).json({ result: response })
  } catch (error) {
    console.error('RAG query error:', error)
    return res.status(500).json({ error: 'Failed to process query' })
  }
}

export default handler
