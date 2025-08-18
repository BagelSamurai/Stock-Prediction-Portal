import { useState } from "react";
import axios from "axios";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const Dashboard = (props) => {
    const [ticker, setTicker] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const [plots, setPlots] = useState(null);
    const [metrics, setMetrics] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        setError(null);
        setPlots(null);
        setMetrics(null);

        try {
            const apiRoot = import.meta.env.VITE_API_ROOT || 'http://127.0.0.1:8000';
            const response = await axios.post(`${apiRoot}/api/v1/predict/`, {
                ticker: ticker
            });

            // Handle logical errors returned from the backend (e.g., invalid ticker)
            if (response.data.error) {
                setError(response.data.error);
                return; // Stop execution if there's a known error
            }

            // Set plots using the backend root URL
            const backendRoot = import.meta.env.VITE_BACKEND_ROOT || 'http://127.0.0.1:8000';
            setPlots({
                original: `${backendRoot}${response.data.plot_img}`,
                ma100: `${backendRoot}${response.data.plot_100dma_img}`,
                ma200: `${backendRoot}${response.data.plot_200dma_img}`,
                final: `${backendRoot}${response.data.plot_final_img}`
            });

            // Set metrics
            setMetrics({
                rmse: response.data.rmse,
                mse: response.data.mse,
                r2Score: response.data.r2Score
            });

        } catch (err) {

            console.error('There was an error making the API request', err);
            setError('Could not connect to the prediction service. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='container'>
            <div className="row">
                <div className="col-md-10 mx-auto text-center">
                    <form onSubmit={handleSubmit}>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Enter Stock Ticker (e.g., AAPL, GOOG)"
                            value={ticker}
                            onChange={(e) => setTicker(e.target.value.toUpperCase())} // Standardize ticker to uppercase
                            required
                        />
                        <button type='submit' className='btn btn-info mt-3' disabled={loading}>
                            {loading ? <span><FontAwesomeIcon icon={faSpinner} spin /> Please wait...</span> : 'See Prediction'}
                        </button>
                    </form>

                    {error && <div className='alert alert-danger mt-3'>{error}</div>}

                    {plots && metrics && (
                        <div className="prediction mt-5">
                            <div className="row">
                                <div className="col-md-6 mb-4">
                                    <img src={plots.original} className="img-fluid" alt="Original vs Prediction" />
                                </div>
                                <div className="col-md-6 mb-4">
                                    <img src={plots.ma100} className="img-fluid" alt="100-day Moving Average" />
                                </div>
                                <div className="col-md-6 mb-4">
                                    <img src={plots.ma200} className="img-fluid" alt="200-day Moving Average" />
                                </div>
                                <div className="col-md-6 mb-4">
                                    <img src={plots.final} className="img-fluid" alt="Final Prediction" />
                                </div>
                            </div>
                            <div className="text-light p-3 mt-4" style={{ backgroundColor: '#111214', borderRadius: '8px' }}>
                                <h3>Model Evaluation</h3>
                                <p>Mean Squared Error (MSE): {metrics.mse}</p>
                                <p>Root Mean Squared Error (RMSE): {metrics.rmse}</p>
                                <p>R-squared: {metrics.r2Score}</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;