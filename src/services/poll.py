from typing import Any

from src.dto import PollRequestDTO, PollResponseDTO
from src.dto.poll import ShortInfoPollResponseDTO, PollUpdateRequestDTO
from src.repositories.poll import PollRepository


class PollService:
    poll_repo = PollRepository()

    def create_poll(self, data: dict[str, Any]):
        try:
            validated_data = PollRequestDTO(**data)

            poll_data = {
                "title": validated_data.title,
                "description": validated_data.description,
                "start_date": validated_data.start_date,
                "end_date": validated_data.end_date,
                "is_active": validated_data.is_active,
                "is_anonymous": validated_data.is_anonymous,
            }

            options = [opt.text for opt in validated_data.options]

            poll, err = self.poll_repo.create_with_options(
                poll_data=poll_data,
                poll_options=options
            )

            if err:
                return None, err

            response = PollResponseDTO.model_validate(poll)

            return response.model_dump_json(indent=4), None

        except Exception as e:
            return None, str(e)

    def get_poll(self, poll_id: int):
        poll, err = self.poll_repo.get_by_id(poll_id)

        if err:
            return None, err

        if not poll:
            return None, f"Not found"

        response = PollResponseDTO.model_validate(poll)

        return response.model_dump_json(indent=4), None

    def get_all_polls(self):
        polls, err = self.poll_repo.get_all()

        if err:
            return None, err


        response = [
            ShortInfoPollResponseDTO.model_validate(
                poll).model_dump_json(indent=4)
            for poll in polls
        ]

        return response, None

    def update_poll(self, poll_id: int, data: dict[str, Any]):
        try:
            validated_data = PollUpdateRequestDTO(**data)

            updated_data = validated_data.model_dump(
                exclude_unset=True,
                exclude_none=True
            )

            if not updated_data:
                return None, "No data to update"

            poll, err = self.poll_repo.update(
                obj_id=poll_id,
                data=updated_data
            )

            if err:
                return None, err

            response = PollResponseDTO.model_validate(poll)

            return response.model_dump_json(indent=4), None

        except Exception as e:
            return None, str(e)

    def delete_poll(self, poll_id: int):
        return self.poll_repo.delete(poll_id)
