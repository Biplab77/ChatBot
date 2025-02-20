export default async function handler(req, res) {
    if (req.method !== "POST") {
      return res.status(405).json({ error: "Method Not Allowed" });
    }
  
    const { userId, text, token } = req.body;
  
    if (!userId || !text || !token) {
      return res.status(400).json({ error: "Missing required fields" });
    }
  
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ user_id: userId, text }),
      });
  
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
  
      const data = await response.json();
      return res.status(200).json(data);
    } catch (error) {
      console.error("Chat API Error:", error.message);
      return res.status(500).json({ error: "Internal Server Error" });
    }
  }
  