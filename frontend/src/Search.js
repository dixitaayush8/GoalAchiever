import React, { Component } from "react";
import "./Search.css";

class Search extends Component {
  state = {
  searchValue: '',
  data: [],
  loading: false
  };

  makeApiCall = searchInput => {
  var searchUrl = 'http://0.0.0.0:5000/api/v1.0/goal';
  this.setState({ loading: true });
  fetch(searchUrl, { headers: {
    'goal': searchInput
     }})
  .then(response => {
  return response.json();
  })
  .then(jsonData => {
  this.setState({ data: jsonData.data, loading: false });
});
  };




// fetch(searchUrl, headers: {
//     "Content-Type": "application/json"
//   }).then(response => {
// return response.json();
// })
// .then(jsonData => {
// console.log(jsonData.keyword);
// });
// };

  handleOnChange = event => {
this.setState({ searchValue: event.target.value });
};

handleKeyPress = event => {
  if (event.charCode === 13){
    event.preventDefault();
    this.handleSearch();
  }
}

handleSearch = () => {
  this.makeApiCall(this.state.searchValue);
}

render() {
  return (
  <div>
  <h1>Goal Achiever</h1>
  <h1></h1>
  <input
    name="text"
    type="text"
    placeholder="Search"
    onChange={event => this.handleOnChange(event)}
    onKeyPress={event => this.handleKeyPress(event)}
    value={this.state.searchValue}
/>
  <button onClick={this.handleSearch}>Search</button>
  {this.state.loading && (
    <p>Loading ...</p>
  )}
  {this.state.data ? (
    <div>
    {this.state.data.map((item, index) => (
    <div key={index}>
    <p>{item.item}</p>
    <h1></h1>
    </div>
    ))}
    </div>
    ) : (
    <p>Try searching for a keyword</p>
    )}
  </div>
  );
}
}
export default Search;
