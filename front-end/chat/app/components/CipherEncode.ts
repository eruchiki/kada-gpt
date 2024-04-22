import crypto from 'crypto';

function encodeBase64(data: string): string {
  const aesKey = process.env.AES_KEY as string;
  const salt = process.env.SALT as string;
  const algo = process.env.ALGORITHM as string;
  const key = crypto.scryptSync(aesKey, salt, 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algo, key, iv);
  const buffData = Buffer.from(data);
  const encData = cipher.update(buffData);
  return Buffer.concat([iv,encData, cipher.final()]).toString('base64');
}

export default encodeBase64;