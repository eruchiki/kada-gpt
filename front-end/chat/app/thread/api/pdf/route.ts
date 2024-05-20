import axios from "axios";

export async function POST(request: Request, res: any) {
  try {
    const docData = await request.json();
    const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections/${docData.CollectionId}/${docData.DocumentId}`;
    const response = await axios.get(url, { responseType: "arraybuffer" });

    return new Response(response.data, {
      status: response.status,
      headers: {
        "Content-Type": response.headers["content-type"],
      },
    });
  } catch (error) {
    console.error("Error:", error);
    return new Response(JSON.stringify({ error: "Something went wrong" }), {
      status: 500,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
}
// import axios from 'axios';

// export default async function handler(req, res) {
//   if (req.method !== 'POST') {
//     res.setHeader('Allow', ['POST']);
//     res.status(405).end(`Method ${req.method} Not Allowed`);
//     return;
//   }

//   const { CollectionId, DocumentId } = req.body;
//   const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections/${CollectionId}/${DocumentId}`;

//   try {
//     const response = await axios.get(url, { responseType: 'arraybuffer' });

//     res.setHeader('Content-Type', 'application/pdf');
//     res.setHeader('Content-Disposition', 'attachment; filename="document.pdf"');
//     res.status(200).send(response.data);
//   } catch (error) {
//     res.status(500).json({ error: 'Failed to download the document' });
//   }
// }
