import { FC } from "react";

export const LoadingIndicator: FC = () => {
  return (
    <div className="absolute inset-0 bg-black/20">
      <div className="loading loading-spinner w-10 h-10 bg-slate-700" />
    </div>
  );
};
