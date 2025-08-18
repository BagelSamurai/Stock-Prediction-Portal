import Button from "./Button.jsx";

const Header =()=> {
    return(
        <nav className='navbar container pt-4 pb-4 align-items-start'>
            <a className="navbar-brand text-light">Stock Prediction Portal</a>
             <p className='text-light lead'>This application utilizes machine learning techniques using Keras and LSTM Model integrated with the Django Framework. It forecases future stock prices by analyzing 100-day and 200-day moving averages, essential indicators widely used by stock analytics to inform trading and investment decisions.</p>

        </nav>
    )
}

export default Header