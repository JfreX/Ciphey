# community
# by https://github.com/lukasgabriel

from typing import Optional, Dict, List

from ciphey.iface import Config, ParamSpec, T, U, Decoder, registry, WordList
from loguru import logger

@registry.register
class Galactic(Decoder[str, str]):
    def decode(self, ctext: T) -> Optional[U]:
        """
        Takes a string written in the 'Standard Galactic Alphabet' 
        (aka Minecraft Enchanting Table Symbols) and translates it to ASCII text.
        """

        logger.trace("Attempting Standard Galactic Alphabet Decoder")
        result = ""
        ctext = (
            ctext.replace("||", "|")
            .replace("/", "")
            .replace("¡", "")
            .replace(" ̣ ", "")
            .replace(" ̇", " x")
        )
        logger.trace(f"Modified string is {ctext}")
        # Take out the problematic characters consisting of multiple symbols
        for letter in ctext:
            if letter in self.GALACTIC_DICT.keys():
                # Match every letter of the input to its galactic counterpoint
                result += self.GALACTIC_DICT[letter]
            else:
                # If the current character is not in the defined alphabet,
                # just accept it as-is (useful for numbers, punctuation,...)
                result += letter

        result = result.replace("x ", "x")
        # Remove the trailing space (appearing as a leading space)
        # from the x that results from the diacritic replacement
        # TODO: Handle edge cases where x still does not show up
        logger.trace(f"Decoded string is {result}")
        return result

    @staticmethod
    def priority() -> float:
        # Not expected to show up often, but also very fast to check.
        return 0.01

    def __init__(self, config: Config):
        super().__init__(config)
        self.GALACTIC_DICT = config.get_resource(
            self._params()["dict"], WordList
        )

    @staticmethod
    def getParams() -> Optional[Dict[str, ParamSpec]]:
        return {
            "dict": ParamSpec(
                desc="The galactic alphabet dictionary to use",
                req=False,
                default="cipheydists::translate::galactic",
            )
        }

    @staticmethod
    def getTarget() -> str:
        return "galactic"
