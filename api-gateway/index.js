const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json());

const MCQ_GEN_SERVICE_URL = process.env.MCQ_GEN_SERVICE_URL || 'http://mcq-gen-service:8001';

// API endpoint để xử lý yêu cầu tạo MCQ
app.post('/api/mcq', upload.single('file'), async (req, res) => {
  try {
    console.log('Received request:', req.body);
    
    const { topic, quantity, difficulty, questionType, numAnswer, isRecheck } = req.body;

    const formData = new FormData();
    formData.append('topic', topic || '');
    formData.append('quantity', quantity || '1');
    formData.append('difficulty', difficulty || 'auto');
    formData.append('type', questionType || 'SingleChoice');
    formData.append('number_of_answers', numAnswer || '4');
    formData.append('recheck', isRecheck === 'true' ? 'true' : 'false');

    // Nếu có file được upload
    if (req.file) {
      console.log('File uploaded:', req.file.originalname);
      const fileStream = fs.createReadStream(req.file.path);
      formData.append('file', fileStream, { filename: req.file.originalname });
    } else if (req.body.inputText) {
      // Nếu không có file nhưng có inputText, lưu thành file tạm
      console.log('Using input text');
      const tempFilePath = path.join(__dirname, 'uploads', Date.now() + '.txt');
      fs.writeFileSync(tempFilePath, req.body.inputText);
      const fileStream = fs.createReadStream(tempFilePath);
      formData.append('file', fileStream, { filename: 'input.txt' });
    }

    console.log('Sending request to MCQ service:', MCQ_GEN_SERVICE_URL);
    
    // Gửi request đến mcq-gen-service
    const response = await axios.post(`${MCQ_GEN_SERVICE_URL}/mcq-gen`, formData, {
      headers: {
        ...formData.getHeaders(),
      },
      timeout: 120000
    });

    console.log('Response received from MCQ service');
    
    // Xóa file tạm sau khi xử lý
    if (req.file) {
      fs.unlinkSync(req.file.path);
    }

    // Xử lý và trả về kết quả
    return res.json({
      notify: `Đã tạo thành công ${response.data.length} câu hỏi.`,
      mcqs: response.data
    });
  } catch (error) {
    console.error('Error in /api/mcq:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
    return res.status(500).json({ 
      error: 'Có lỗi xảy ra trong quá trình xử lý.',
      details: error.message 
    });
  }
});

// Tạo thư mục uploads nếu chưa tồn tại
if (!fs.existsSync(path.join(__dirname, 'uploads'))) {
  fs.mkdirSync(path.join(__dirname, 'uploads'));
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API Gateway đang chạy tại http://localhost:${PORT}`);
});