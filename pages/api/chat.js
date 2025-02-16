export default async function handler(req, res) {
    // Allow only POST requests
    if (req.method !== "POST") {
      return res.status(405).json({ error: "Method Not Allowed" });
    }
  
    // Extract data from request body
    const { userId, text, token } = req.body;
  
    try {
      // Send request to FastAPI backend
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ user_id: userId, text }),
      });
  
      // Parse the response
      const data = await response.json();
  
      // Handle errors if FastAPI fails
      if (!response.ok) {
        return res.status(response.status).json({ error: data.detail || "Chatbot error" });
      }
  
      // Send chatbot response back to the frontend
      return res.status(200).json(data);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      return res.status(500).json({ error: "Internal Server Error" });
    }
  }
  