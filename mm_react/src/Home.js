import React, { useState } from 'react';

function Home() {
  const [showList, setShowList] = useState(false);
  const [selectedItem, setSelectedItem] = useState('Dashboard');

  function handleButtonClick() {
    setShowList(!showList);
  }

  function handleItemClick(item) {
    setSelectedItem(item);
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <button className="navbar-toggler" type="button" onClick={handleButtonClick}>
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Profile
                </a>
                <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                  <li><a className="dropdown-item" href="#">Action</a></li>
                  <li><a className="dropdown-item" href="#">Another action</a></li>
                  <li><hr className="dropdown-divider" /></li>
                  <li><a className="dropdown-item" href="#">Something else here</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className="container">
        <h1>Hello, Home Page</h1>
        <div className="btn-group">
          <button type="button" className="btn btn-primary" onClick={handleButtonClick}>
            {showList ? 'Close' : 'Open'}
          </button>
        </div>
        {showList && (
          <ul className="list-group mt-3">
            <li className={`list-group-item ${selectedItem === 'Dashboard' ? 'active' : ''}`} onClick={() => handleItemClick('Dashboard')}>
              Dashboard
            </li>
            <li className={`list-group-item ${selectedItem === 'Income' ? 'active' : ''}`} onClick={() => handleItemClick('Income')}>
              Income
            </li>
            <li className={`list-group-item ${selectedItem === 'Expenses' ? 'active' : ''}`} onClick={() => handleItemClick('Expenses')}>
              Expenses
            </li>
          </ul>
        )}
      </div>
    </div>
  );
}

export default Home;
