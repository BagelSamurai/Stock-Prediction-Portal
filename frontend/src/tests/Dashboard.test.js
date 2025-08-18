import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import Dashboard from "../components/Dashboard.jsx";

// Mock the axios module
jest.mock('axios');

describe('Dashboard Component', () => {
  test('renders form input and submit button', () => {
    render(<Dashboard />);

    // Check if the input field is rendered
    expect(screen.getByPlaceholderText(/Enter Stock Ticker/i)).toBeInTheDocument();

    // Check if the button is rendered
    expect(screen.getByRole('button', { name: /See Prediction/i })).toBeInTheDocument();
  });

  test('handles form submission, shows loading state, and displays results', async () => {
    // Mock a successful API response
    const mockResponse = {
      data: {
        status: 'success',
        plot_img: '/media/AAPL_plot.png',
        plot_100dma_img: '/media/AAPL_100dma_plot.png',
        plot_200dma_img: '/media/AAPL_200dma_plot.png',
        plot_final_img: '/media/AAPL_final_plot.png',
        mse: 10.5,
        rmse: 3.24,
        r2Score: 0.95,
      },
    };
    axios.post.mockResolvedValue(mockResponse);

    render(<Dashboard />);

    const input = screen.getByPlaceholderText(/Enter Stock Ticker/i);
    const button = screen.getByRole('button', { name: /See Prediction/i });

    // Simulate user typing a ticker and clicking the button
    fireEvent.change(input, { target: { value: 'AAPL' } });
    fireEvent.click(button);

    // Check for loading state
    expect(screen.getByText(/Please wait.../i)).toBeInTheDocument();
    expect(button).toBeDisabled();

    // Wait for the results to be displayed
    await waitFor(() => {
      // Check if one of the images is rendered
      expect(screen.getByAltText(/Final Prediction/i)).toBeInTheDocument();
      // Check if one of the metrics is displayed
      expect(screen.getByText(/Mean Squared Error \(MSE\): 10.5/i)).toBeInTheDocument();
    });

    // Ensure the loading spinner is gone
    expect(screen.queryByText(/Please wait.../i)).not.toBeInTheDocument();
    expect(button).not.toBeDisabled();
  });

  test('displays an error message on API failure', async () => {
    // Mock a failed API response
    axios.post.mockRejectedValue(new Error('Network Error'));

    render(<Dashboard />);

    fireEvent.change(screen.getByPlaceholderText(/Enter Stock Ticker/i), { target: { value: 'FAIL' } });
    fireEvent.click(screen.getByRole('button', { name: /See Prediction/i }));

    // Wait for the error message to appear
    await waitFor(() => {
      expect(screen.getByText(/Could not connect to the prediction service/i)).toBeInTheDocument();
    });
  });
});
