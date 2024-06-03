import { Suspense } from "react";
const SuspenseWrapper = (Component: () => JSX.Element) => (props: any) => {
  return (
    <Suspense fallback={<>loading...</>}>
      <Component {...props} />
    </Suspense>
  );
};

export default SuspenseWrapper;
