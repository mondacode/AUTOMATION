"use client"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2 } from "lucide-react"

export default function QueryRAG() {
  const [query, setQuery] = useState("")
  const [response, setResponse] = useState("")
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const handleQuery = async () => {
    setLoading(true)
    setResponse("")
    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      setResponse(data.result)
      setHistory(prev => [{ query, answer: data.result }, ...prev])
    } catch {
      setResponse("Error retrieving result.")
    }
    setLoading(false)
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-4xl font-bold tracking-tight">RAG Query Interface</h1>
      <div className="space-y-2">
        <Input
          placeholder="Ask a question about your documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="text-base"
        />
        <Button onClick={handleQuery} disabled={loading} className="w-full">
          {loading && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
          Ask
        </Button>
      </div>
      {response && (
        <Card>
          <CardContent className="p-4">
            <Textarea value={response} readOnly rows={10} className="resize-none" />
          </CardContent>
        </Card>
      )}
      {history.length > 0 && (
        <div className="space-y-2">
          <h2 className="text-xl font-semibold">Query History</h2>
          {history.map((item, index) => (
            <Card key={index}>
              <CardContent className="p-4 space-y-1">
                <p className="text-sm font-medium text-muted-foreground">Q: {item.query}</p>
                <p className="text-sm">A: {item.answer}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
