from flask import jsonify, request
from http import HTTPStatus

from src.services.poll import PollService


class PollController:
    poll_service = PollService()
    # CRUD for Poll

    def create_poll(self):
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "No data provided"
                }
            ), HTTPStatus.BAD_REQUEST

        poll, err = self.poll_service.create_poll(data=data)

        if err:
            return jsonify({
                "status": 'error',
                "message": err
            }), HTTPStatus.BAD_REQUEST

        return jsonify({
            "status": 'success',
            "data": poll
        }), HTTPStatus.CREATED

    def get_poll_by_id(self, poll_id: int):
        poll, err = self.poll_service.get_poll(poll_id=poll_id)

        if err:
            return jsonify({
                "status": 'error',
                "message": err
            }), HTTPStatus.NOT_FOUND if err == "Not found" else HTTPStatus.BAD_REQUEST

        return jsonify({
            "status": 'success',
            "data": poll
        }), HTTPStatus.OK  # 200

    def get_polls(self):
        polls, err = self.poll_service.get_all_polls()

        if err:
            return jsonify({
                "status": 'error',
                "message": err
            }), HTTPStatus.INTERNAL_SERVER_ERROR  # 500

        return jsonify({
            "status": 'success',
            "data": polls
        }), HTTPStatus.OK

    def update_poll(self, poll_id: int):
        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "No data provided"
                }
            ), HTTPStatus.BAD_REQUEST

        poll, err = self.poll_service.update_poll(
            poll_id=poll_id,
            data=data
        )

        if err:
            return (jsonify({
                "status": 'error',
                "message": err
            }), HTTPStatus.NOT_FOUND if err == f"{self.poll_service.poll_repo.model_class.__name__} not found"
            else HTTPStatus.BAD_REQUEST)

        return jsonify({
            "status": 'success',
            "data": poll
        }), HTTPStatus.OK

    def delete_poll(self, poll_id: int):
        success, err = self.poll_service.delete_poll(poll_id=poll_id)

        if err:
            return (jsonify({
                "status": 'error',
                "message": err
            }), HTTPStatus.NOT_FOUND if err == f"{self.poll_service.poll_repo.model_class.__name__} not found"
            else HTTPStatus.BAD_REQUEST)

        return jsonify({
            "status": 'success',
        }), HTTPStatus.NO_CONTENT
