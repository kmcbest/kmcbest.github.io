// api/watchlist.js
export default async function handler(req, res) {
    // 从 Vercel 自动注入的环境变量里读取数据库连接钥匙
    const token = process.env.KV_REST_API_TOKEN;
    const url = process.env.KV_REST_API_URL;

    // 简单设置一个防刷密码（暗号），后面在 HTML 头部带上
    // 如果别人知道了接口路径，但没有这个暗号，就会被拒绝，保障你的女优数据安全
    const ACCESS_PASSWORD = "my_private_secret_key_999";
    const userPassword = req.headers['x-watchlist-auth'];

    if (userPassword !== ACCESS_PASSWORD) {
        return res.status(401).json({ error: "暗号不正确，拒绝访问！" });
    }

    try {
        // ==========================================
        // 1. 处理读取请求 (GET)
        // ==========================================
        if (req.method === 'GET') {
            // 通过 Vercel 内网环境请求 Upstash 数据库，获取键名为 data 的内容
            const response = await fetch(`${url}/get/data`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const result = await response.json();
            
            // Upstash 返回的格式是 { result: "你的字符串数据" }
            // 如果数据库是空的，result 会是 null
            const actualData = result.result ? JSON.parse(result.result) : null;
            return res.status(200).json(actualData);
        }

        // ==========================================
        // 2. 处理写入请求 (POST)
        // ==========================================
        if (req.method === 'POST') {
            const bodyData = req.body; // 拿到前端发过来的整个 JSON 字符串
            
            // 调用 Upstash 标准的 /set/data 接口把数据存进去
            const response = await fetch(`${url}/set/data`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(bodyData)
            });
            const result = await response.json();
            return res.status(200).json({ success: true, result });
        }

        // 其余不受支持的请求方法
        return res.status(405).json({ error: "Method not allowed" });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
}