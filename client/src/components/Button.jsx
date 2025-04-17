export function ButtonPrimary({children, classes, action = () => {}}) {
  return (
    <button onClick={action} className={classes + " inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md font-semibold text-xs uppercase tracking-widest text-white bg-indigo-700 hover:bg-indigo-900 active:bg-gray-900 focus:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition ease-in-out duration-150"}>
      {children}
    </button>
  );
}

export function ButtonSecondary({children, classes, action = () => {}}) {
  return (
    <button onClick={action} className={classes + " inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md font-semibold text-xs uppercase tracking-widest text-black bg-orange-500 hover:bg-orange-600 active:bg-orange-800 focus:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 transition ease-in-out duration-150"}>
      {children}
    </button>
  );
}