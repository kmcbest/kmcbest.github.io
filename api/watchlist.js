// api/watchlist.js
export default async function handler(req, res) {
    const token = process.env.KV_REST_API_TOKEN;
    const url = process.env.KV_REST_API_URL;

    const ACCESS_PASSWORD = "my_private_secret_key_999";
    const userPassword = req.headers['x-watchlist-auth'];

    if (userPassword !== ACCESS_PASSWORD) {
        return res.status(401).json({ error: "暗号不正确，拒绝访问！" });
    }

    // 【核心改动】动态获取前端指定的存储键名，如果没传，默认用老项目的 'data'
    const storageKey = req.headers['x-watchlist-key'] || 'data';

    try {
        // ==========================================
        // 1. 处理读取请求 (GET)
        // ==========================================
        if (req.method === 'GET') {
            // 这里的路径动态带上了 storageKey
            const response = await fetch(`${url}/get/${storageKey}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const result = await response.json();
            
            const actualData = result.result ? JSON.parse(result.result) : null;
            return res.status(200).json(actualData);
        }

        // ==========================================
        // 2. 处理写入请求 (POST)
        // ==========================================
        if (req.method === 'POST') {
            const bodyData = req.body;
            
            // 这里的路径动态带上了 storageKey
            const response = await fetch(`${url}/set/${storageKey}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(bodyData)
            });
            const result = await response.json();
            return res.status(200).json({ success: true, result });
        }

        return res.status(405).json({ error: "Method not allowed" });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
}