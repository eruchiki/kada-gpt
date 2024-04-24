import * as crypto from 'crypto'


function DecodeBase64(data: string): string {
    const key = crypto.scryptSync(process.env.AES_KEY  as string,process.env.SALT as string,32)
    const buff = Buffer.from(data, 'base64');
    const iv = buff.slice(0, 16);
    const encData = buff.slice(16);
    const decipher = crypto.createDecipheriv(process.env.ALGORITHM as string, key, iv);
    const decData = decipher.update(encData);
    return Buffer.concat([decData, decipher.final()]).toString('utf8');
}
    
export default DecodeBase64
