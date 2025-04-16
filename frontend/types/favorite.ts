export interface FavoriteItem {
  id: string;
  analysis_id: string;
  input_text: string;
  result_json: string;
  created_at: string;
  download_url?: string;
  pdf_filename?: string;
} 