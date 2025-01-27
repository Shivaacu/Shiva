import React, { useState, useEffect } from 'react';

function MissingItems() {
  const [missingItems, setMissingItems] = useState([]);

  useEffect(() => {
    const fetchMissingItems = async () => {
      const response = await fetch('http://localhost:5000/api/get_missing_items');
      const data = await response.json();
      setMissingItems(data);
    };

    fetchMissingItems();
    const interval = setInterval(fetchMissingItems, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Missing Items</h2>
      <ul>
        {missingItems.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default MissingItems;
