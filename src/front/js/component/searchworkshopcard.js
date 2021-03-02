import React, { Component, useContext } from "react";
import { Context } from "../store/appContext";
import PropTypes from "prop-types";

import { YellowButton } from "./yellowButton";
import { DeleteButton } from "./deleteButton";
import { EditButton } from "./editButton";

export const WorkshopCard = props => {
	const { actions, store } = useContext(Context);

	return (
		<div className="searchWorkshopCard">
			<div className="cardInformation">
				<div className="details">
					<span className="date">Date: {props.item.date}</span>
					<span className="duration">Duration: {props.item.duration} hours</span>
					<span className="pax">Pax: {props.item.max_people}</span>
					<span className="category">Category: </span>
				</div>
			</div>
			<div className="buttons_workshopCard">
				<EditButton className="editButton_workshopCard" />
				<DeleteButton className="deleteButton_workshopCard" />
				<YellowButton className="yellowButton_workshopCard" />
			</div>
		</div>
	);
};

WorkshopCard.propTypes = {
	item: PropTypes.object,
};
