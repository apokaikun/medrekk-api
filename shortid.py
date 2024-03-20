import binascii
import math
import os
import string
from typing import List, Optional


def int_to_string(
    randnum: int, alphabet: List[str], padding: Optional[int] = None
) -> str:
    """
    Convert a random number (randnum) to a string, using the given alphabet.

    """
    output = ""
    output_ = ""
    alpha_len = len(alphabet)
    while randnum and len(output) < 12:
        randnum, digit = divmod(randnum, alpha_len)
        output = alphabet[digit] + output

    return output


class ShortRandomID:
    """ """

    def __init__(
        self, alpha: Optional[str] = None, random_size: Optional[int] = None
    ) -> None:
        """ """
        alpha = alpha if alpha else string.ascii_letters + string.digits
        self.set_alpha(alpha)

        size = random_size if random_size else 128
        self.set_random_size(size)

    @property
    def _alpha_len(self) -> int:
        return len(self._alpha)

    @property
    def _length(self) -> int:
        """
        The effective length of the ID given the set alphabet.
        """
        size = 2**self._random_length
        return int(math.ceil(math.log(size, self._alpha_len)))

    def set_random_size(self, size: int) -> None:
        """
        Sets the size of the string which represents random bytes suitable for cryptographic use.
        """
        if size < 0:
            raise ValueError("Must be set to non-negative integer.")

        self._random_length = size

    def get_alpha(self):
        """
        Return the set of characters/symbols to be used for the random IDs.
        """
        return self._alpha

    def set_alpha(self, alpha: str) -> None:
        """
        Sets the characters/symbols to be used for the random IDs.
        Default is set to `string.ascii_letters` + `string.digits`'
        """
        new_alpha = "".join(set(alpha))
        if len(new_alpha) > 1:
            self._alpha = new_alpha
        else:
            raise ValueError("Length of characters must be more the one (1).")

    def random(self, length: Optional[int] = None) -> str:
        """ """
        if length is None:
            length = self._length

        random_int = int(binascii.b2a_hex(os.urandom(length)), 16)
        alphabet = self._alpha

        output = ""

        while random_int and len(output) < length:
            random_int, index = divmod(random_int, self._alpha_len)
            output += alphabet[index]

        padding = max(length - len(output), 0)

        output = output + output[-1] * padding
        return output[:length]
