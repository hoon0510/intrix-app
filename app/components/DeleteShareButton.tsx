import React from 'react';
import { toast } from 'react-toastify';

interface DeleteShareButtonProps {
  shareUuid: string;
  onDelete: () => void;
}

export default function DeleteShareButton({ shareUuid, onDelete }: DeleteShareButtonProps) {
  const handleDelete = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/share/${shareUuid}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete share link');
      }

      toast.success('공유 링크가 삭제되었습니다');
      onDelete();
    } catch (error) {
      console.error('Error deleting share link:', error);
      toast.error('공유 링크 삭제에 실패했습니다');
    }
  };

  return (
    <button
      onClick={handleDelete}
      className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
    >
      공유 삭제
    </button>
  );
} 