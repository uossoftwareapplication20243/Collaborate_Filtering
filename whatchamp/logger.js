// logger.js
const winston = require('winston');
const path = require('path');

// 로그 디렉토리 생성 (필요 시)
const logDirectory = path.join(__dirname, 'logs');

// 로거 설정
const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug', // 환경별 로그 레벨 설정
  format: winston.format.combine(
    winston.format.timestamp({
      format: 'YYYY-MM-DD HH:mm:ss',
    }),
    winston.format.printf(({ timestamp, level, message }) => `${timestamp} [${level.toUpperCase()}]: ${message}`)
  ),
  transports: [
    // 콘솔 출력
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(), // 색상 적용
        winston.format.printf(({ timestamp, level, message }) => `${timestamp} [${level}]: ${message}`)
      ),
      silent: process.env.NODE_ENV === 'production', // 운영 환경에서는 콘솔 로그 비활성화
    }),
    // 파일 저장 (전체 로그)
    new winston.transports.File({
      filename: path.join(logDirectory, 'combined.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 5,
      tailable: true,
    }),
    // 파일 저장 (에러 로그)
    new winston.transports.File({
      filename: path.join(logDirectory, 'error.log'),
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5,
      tailable: true,
    }),
  ],
  exceptionHandlers: [
    new winston.transports.File({ filename: path.join(logDirectory, 'exceptions.log') })
  ],
  exitOnError: false, // 예외 발생 시 프로세스 종료하지 않음
});

module.exports = logger;
