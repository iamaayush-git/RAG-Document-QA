// backend/src/index.js
import express from "express";
import cors from "cors";
import filesRouter from "./routes/files.js";
import queryRouter from "./routes/query.js";
import morgan from "morgan";

const app = express();
app.use(cors());
app.use(express.json());
app.use(morgan("dev"));

app.use("/api/files", filesRouter);
app.use("/api/query", queryRouter);

// generic error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({
    success: false,
    error: { message: err.message || "Internal Server Error" },
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Node backend running on http://localhost:${PORT}`));
