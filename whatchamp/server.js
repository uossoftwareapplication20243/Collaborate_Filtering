const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const iconv = require('iconv-lite');
const logger = require('./logger'); // 로거 모듈 가져오기
const app = express();
const port = 3000;

// JSON 파싱 미들웨어 설정
app.use(express.json());

// 정적 파일 경로 설정
app.use(express.static(path.join(__dirname, 'build')));

// API 엔드포인트 설정
app.post('/api/starter', (req, res) => {
  const { username, tag } = req.body;
  
  if (!username || !tag) {
    // 잘못된 요청일 때 (예: 필수 데이터가 없을 때)
    return res.status(400).json({ message: "Invalid request: username and tag are required" });
  }

  const scriptPath = path.join(__dirname, 'python', 'riot_name_api.py');  // 예시: 현재 디렉토리 기준으로 python 폴더 내부
  const pythonProcess = spawn('python', [scriptPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // JSON 데이터를 UTF-8로 인코딩하여 Python 스크립트의 stdin으로 전달
  const jsonString = JSON.stringify(req.body);
  logger.debug(`Sending to Python script: ${jsonString}`); // Python으로 보내는 데이터 확인

  pythonProcess.stdin.write(jsonString, 'utf-8');
  pythonProcess.stdin.end();

  // Python 스크립트 결과 수신
  let data = '';
  pythonProcess.stdout.on('data', (chunk) => {
    const chunkStr = chunk.toString();
    logger.debug(`Python response chunk: ${chunkStr}`);
    data += chunkStr;
  });

  pythonProcess.stdout.on('end', () => {
    try {
      const responseData = JSON.parse(data);
      logger.info(`Sending response to client: ${JSON.stringify(responseData)}`);

      if (data > 50) {
        res.status(200).json({ 
          message: "Data processed successfully",
          "record-based": true });
      } else {
        res.status(200).json({ message: "Data processed, but without record", "record-based": false });
      }
    } catch (err) {
      logger.error(`Error parsing Python response: ${err.message}`);
      res.status(500).json({ message: 'Python script error', error: err.message });
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    const errorStr = data.toString();
    logger.error(`Python error: ${errorStr}`);
  });

  pythonProcess.on('error', (err) => {
    logger.error(`Failed to start Python process: ${err.message}`);
    res.status(500).json({ message: 'Failed to start Python process', error: err.message });
  });
});



app.get('/api/result/:username/:tag', (req, res) => {
  const { username, tag } = req.params;
  const { line } = req.query;

  if (!username || !tag || !line) {
    return res.status(400).json({ message: 'Invalid request: username, tag, and line are required' });
  }

  let champions = ['아트록스', '아리', '그라가스'];


  // python spawn



  res.status(200).json({
    message: 'Data processed successfully',
    champions: champions, // 클라이언트로 전송할 champions 데이터
    'record-based': true, // 예시로 추가한 필드
  });
});


// API 엔드포인트 설정
app.post('/api/new/result', (req, res) => {
  // 클라이언트에서 전달된 JSON 데이터 (questionMap)를 받아옴
  const questionMap = req.body;
  logger.info(`Received questionMap: ${JSON.stringify(questionMap)}`); // 클라이언트로부터 받은 데이터 확인

  const scriptPath = path.join(__dirname, 'python', 'cossim.py');  // 예시: 현재 디렉토리 기준으로 python 폴더 내부
  const pythonProcess = spawn('python', [scriptPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // JSON 데이터를 UTF-8로 인코딩하여 Python 스크립트의 stdin으로 전달
  const jsonString = JSON.stringify(questionMap);
  logger.debug(`Sending to Python script: ${jsonString}`); // Python으로 보내는 데이터 확인

  pythonProcess.stdin.write(jsonString, 'utf-8');
  pythonProcess.stdin.end();

  // Python 스크립트 결과 수신
  let data = '';
  pythonProcess.stdout.on('data', (chunk) => {
    const chunkStr = chunk.toString();
    logger.debug(`Python response chunk: ${chunkStr}`);
    data += chunkStr;
    // data += iconv.decode(chunk, 'euc-kr');
  });

  pythonProcess.stdout.on('end', () => {
    try {
      const responseData = JSON.parse(data.toString('utf-8'));
      logger.info(`Sending response to client: ${JSON.stringify(responseData)}`);
      res.json(responseData);
    } catch (err) {
      logger.error(`Error parsing Python response: ${err.message}`);
      res.status(500).json({ message: 'Python script error', error: err.message });
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    const errorStr = data.toString();
    logger.error(`Python error: ${errorStr}`);
  });

  pythonProcess.on('error', (err) => {
    logger.error(`Failed to start Python process: ${err.message}`);
    res.status(500).json({ message: 'Failed to start Python process', error: err.message });
  });
});

// 모든 라우트를 index.html로 리다이렉트
app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// 서버 포트 설정
app.listen(port, () => {
  logger.info(`Server is running on http://(public_ip4):${port}`);
});
