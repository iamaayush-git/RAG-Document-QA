// backend/src/routes/files.js
import express from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import { callPythonIngest } from "../services/pythonClient.js";

const router = express.Router();
const uploadDir = path.resolve(process.cwd(), "uploads");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (_, __, cb) => cb(null, uploadDir),
  filename: (_, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});
const upload = multer({ storage });

router.post("/upload", upload.single("file"), async (req, res, next) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, error: { message: "No file uploaded" } });
    const filepath = req.file.path;
    // call python service to ingest
    const ingestRes = await callPythonIngest(filepath);
    res.json({ success: true, filename: req.file.filename, ingest: ingestRes });
  } catch (err) {
    next(err);
  }
});

router.get("/", (req, res) => {
  const files = fs.readdirSync(uploadDir).map((f) => ({ filename: f, uploadedAt: fs.statSync(path.join(uploadDir, f)).mtime }));
  res.json({ success: true, files });
});

export default router;
