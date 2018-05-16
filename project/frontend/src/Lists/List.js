import React, { Component } from 'react';
import { connect } from 'react-redux'

import './Lists.css'

import moment from 'moment';


function itemsUl(d) {
  return (
    <ul>
    { d['items'].map(itemLi) }
    </ul>
    )
}
function itemLi(d, idx) {
  return (
    <li key={idx} className={d.checked?'checked':''}>
    {d.content}
    {d.items.length ? itemsUl(d) : null}
    </li>
    );
}

class List extends Component {

constructor(props){
  super(props)
}

render() {
  let list = this.props.lists.find(l => l['name']==this.props.name)

  if (!list) return null;

  let content = (<span>Nothing here</span>);
  if (list['items'].length) {
    content = (
      itemsUl(list)
    )
  }

  return (
    <div className="List">
    <h2>{list['name']}</h2>
    {content}
    </div>)
}

}



const mapStateToProps = (state) => ({
  lists: state.lists,
})
const ConnectedList = connect(
  mapStateToProps,
  null
)(List)


export default ConnectedList