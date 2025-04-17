const Footer = () => {
  return (
    <footer className="w-full border-t text-center py-6 text-xs text-gray-500 mt-10">
      <p>© 2025 Intrix. All rights reserved.</p>
      <p className="mt-1">
        <a href="/terms" className="underline mr-2">
          이용약관
        </a>
        |
        <a href="/privacy" className="underline ml-2">
          개인정보처리방침
        </a>
      </p>
    </footer>
  );
};

export default Footer; 