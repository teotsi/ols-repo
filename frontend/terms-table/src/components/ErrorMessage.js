const ErrorMessage = () => {
  return (
    <div className="error-message">
      <h2>⚠️ Something went wrong ⚠️</h2>
      <p>
        Fetching the EFO terms was not successful. Check the error on your
        console for any leads. <br />
        Verify that:
      </p>
      <ol className="list">
        <li>The backend server is running.</li>
        <li>
          The backend server <code>DOMAIN</code> environment variable is set
          correctly on the <code>.env</code> file. If you're unsure what this
          means, check the <code>README.md</code> under{" "}
          <code>frontend /terms-table</code>.
        </li>
        <li>
          If you get a CORS error, just update the CORS configuration as per the{" "}
          <code>README.md</code> under <code>frontend /terms-table</code>.
        </li>
      </ol>
    </div>
  );
};

export default ErrorMessage;
