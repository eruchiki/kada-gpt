// "use client";
// import React from "react";
// import { useState } from "react";

// const PdfForm = () => {
//   const [files, setFiles] = useState([]);

//   const handleDrop = (e) => {
//     e.preventDefault();
//     const newFiles = [...e.dataTransfer.files];
//     setFiles([...files, ...newFiles]);
//   };

//   const handleFileChange = (e) => {
//     const newFiles = [...e.target.files];
//     setFiles([...files, ...newFiles]);
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     // ファイルのアップロード処理を行う
//     console.log(files);
//   };

//   return (
//     <div>
//       <h1>PDF ファイルをアップロード</h1>
//       <form
//         onSubmit={handleSubmit}
//         onDrop={handleDrop}
//         encType="multipart/form-data"
//       >
//         <input type="file" multiple accept=".pdf" onChange={handleFileChange} />
//         <button type="submit">アップロード</button>
//       </form>
//       <ul>
//         {files.map((file, index) => (
//           <li key={index}>{file.name}</li>  
//         ))}
//       </ul>
//     </div>
//   );
// }


// export default PdfForm