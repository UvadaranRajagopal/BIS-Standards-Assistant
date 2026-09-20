import { Upload, FileText } from "lucide-react";
import { useRef, useState } from "react";

interface Props {
  onFileSelect: (file: File) => void;
}

export default function FileUpload({
  onFileSelect,
}: Props) {

  const inputRef = useRef<HTMLInputElement>(null);

  const [fileName, setFileName] = useState("");

  const handleFile = (file?: File) => {

    if (!file) return;

    if (file.type !== "application/pdf") {
      alert("Please upload a PDF file.");
      return;
    }

    setFileName(file.name);

    onFileSelect(file);
  };


  return (
    <div>

      <div
        className="upload-box"
        onClick={() => inputRef.current?.click()}
      >

        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          hidden
          onChange={(e) =>
            handleFile(e.target.files?.[0])
          }
        />

        <div className="upload-icon">
          <Upload size={30} />
        </div>

        <h3>Upload Tender / Requirement PDF</h3>

        <p>
          Click to browse and select a PDF document
        </p>

        <span>
          PDF files only
        </span>

      </div>

      {fileName && (

        <div className="selected-file">

          <FileText size={20} />

          <div>
            <strong>{fileName}</strong>
            <small>Ready for analysis</small>
          </div>

        </div>

      )}

    </div>
  );
}