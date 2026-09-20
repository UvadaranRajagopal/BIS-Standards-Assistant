import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface RelatedStandard {
  id: string;

  document: string;

  metadata: {
    is_number: string;
    title: string;
    category: string;
    year?: number;
    status?: string;
  };

  distance: number;
}

export interface VersionCheck {
  standard_id: string;
  current_version?: number | string;
  dataset_version?: number | string;
  status: string;
  message: string;
}

export interface StandardResult {
  id: string;

  document: string;

  metadata: {
    is_number: string;
    title: string;
    category: string;
    year?: number;
    status?: string;
    certification?: string;
  };

  distance: number;

  relevance_score: number;

  version_check?: VersionCheck;

  related_standards?: RelatedStandard[];
}

export interface AnalyzeResponse {
  query: string;
  standards: StandardResult[];
  explanation: string;
}

export const standardsApi = {
  analyze: async (
    query: string,
    topK: number = 3
  ): Promise<AnalyzeResponse> => {
    const response = await api.post(
      "/standards/analyze",
      {
        query,
        top_k: topK,
      }
    );

    return response.data;
  },

  accept: async (
    tenderId: string,
    officerId: string,
    acceptedStandards: string[],
    verified: boolean,
    certificationVerifications: Record<string, boolean>
  ) => {
    const response = await api.post(
      "/standards/accept",
      {
        tender_id: tenderId,
        officer_id: officerId,
        accepted_standards: acceptedStandards,
        verified,
        certification_verifications:
          certificationVerifications,
      }
    );

    return response.data;
  },
};

export const auditApi = {
  getLogs: async () => {
    const response =
      await api.get("/audit/logs");

    return response.data;
  },

  verifyIntegrity: async () => {
    const response =
      await api.get("/audit/verify");

    return response.data;
  },
};


/* ================================
   PDF API
================================ */

export const pdfApi = {
  extract: async (file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
      "/pdf/extract",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  },
};