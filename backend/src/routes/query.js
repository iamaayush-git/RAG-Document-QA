// backend/src/routes/query.js
import express from "express";
import { callPythonAsk } from "../services/pythonClient.js";
const router = express.Router();

router.post("/", async (req, res, next) => {
  try {
    const { question } = req.body;
    if (!question) return res.status(400).json({ success: false, error: { message: "question required" } });

    const result = await callPythonAsk(question, 4); // default k=4
    res.json({ success: true, ...result });
  } catch (err) {
    next(err);
  }
});

export default router;
