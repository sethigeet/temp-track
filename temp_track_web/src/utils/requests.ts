import { useQuery } from "react-query";

function getStatus(loc: string) {
  fetch(`/api/status/${loc}`).then((res) => res.json());
}

export function useGetStatusQuery(loc: string) {
  return useQuery(`get_status:${loc}`, () => getStatus(loc), {
    refetchInterval: 10 * 60,
    cacheTime: 10 * 60,
    // enabled: false,
  });
}
