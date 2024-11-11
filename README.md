# front-back 사전준비

whatchamp/src/const/url.js 에서 url 수정해주세요!
port도 수정할 시 whatchamp/server.js 에서 port도 수정해주세요!

# react, nodejs 실행

0. 프로젝트 위치에 이동, npm install
1. npm run build (react set build)
2. node server

# collaborate filtering python 적용

whatchamp/server.js 에서

```javascript
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

```

예시로 app.post('/api/new/result', (req, res)에서는 다음과 같이 사용하고 있음.

```javascript
  const scriptPath = path.join(__dirname, 'python', 'cossim.py');  // 예시: 현재 디렉토리 기준으로 python 폴더 내부
  const pythonProcess = spawn('python', [scriptPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

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
```
