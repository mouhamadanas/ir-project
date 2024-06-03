import { UseQuery } from "@reduxjs/toolkit/dist/query/react/buildHooks";
import { useEffect, useState } from "react";

export const usePaginateData = (hook: UseQuery<any>, params: any) => {
  const [totalRecords, setTotalRecords] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const { data, isLoading, isFetching, isError, isSuccess, refetch } =
    hook(params);
  const transformData: any = data;

  useEffect(() => {
    !isLoading ? setTotalRecords(transformData?.totalRecords) : null;
  }, [isLoading]);

  const changePage = (pageNumber: number) => {
    setPage(pageNumber);
  };

  const handleDelete = () => {
    setTotalRecords((prev) => prev ?? 1 - 1);
  };

  return {
    data,
    isLoading,
    isFetching,
    isError,
    isSuccess,
    refetch,
    totalRecords,
    page,
    changePage,
    handleDelete,
  };
};
