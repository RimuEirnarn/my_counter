from lymia import Scene, on_key, run, status
from lymia.environment import Theme
from lymia.colors import Coloring, ColorPair, color
from lymia.data import ReturnType

class Basic(Coloring):
    AWESOME = ColorPair(color.BLUE, color.BLACK)
    GOOD = ColorPair(color.GREEN, color.BLACK)
    NORMAL = ColorPair(color.WHITE, color.BLACK)
    BAD = ColorPair(color.YELLOW, color.BLACK)
    AWFUl = ColorPair(color.RED, color.BLACK)

class Root(Scene):
    use_default_color = True
    
    def __init__(self) -> None:
        super().__init__()
        self._table = {
            "Awesome": 0,
            "Good": 0,
            "Normal": 0,
            "Bad": 0,
            "Awful": 0
        }
        self._last_keys: list[str] = []
        self._last_ptr = 0
        self._ln = max(tuple(map(len, tuple(self._table.keys()))))

    def _push(self, key: str):
        if len(self._last_keys) == self._last_ptr:
            self._last_keys.append(key)
        else:
            if self._last_keys[self._last_ptr] != key:
                self._last_keys = self._last_keys[:self._last_ptr]
                self._last_keys.append(key)
            else:
                self._last_keys.append(key)
        self._last_ptr += 1
        self._table[key] += 1
        status.set('')

    def _undo(self):
        if self._last_ptr == 0:
            status.set("No undo can be done!")
            return
        self._last_ptr -= 1
        try:
            pop = self._last_keys[self._last_ptr]
        except IndexError as exc:
            exc.add_note(f"Len: {len(self._last_keys)} <-- {self._last_ptr}")
            raise exc
        self._table[pop] -= 1

    def _redo(self):
        if self._last_ptr == len(self._last_keys):
            status.set("Already in present.")
            return
        try:
            pop = self._last_keys[self._last_ptr]
        except IndexError as exc:
            exc.add_note(f"Len: {len(self._last_keys)} <-- {self._last_ptr}")
            raise exc
        self._last_ptr += 1
        self._table[pop] += 1

    def draw(self) -> None | ReturnType:
        self._screen.addstr("Count your recorded days. This is to manually import from Samsung Health / Mood Check-in")
        
        for index, (key, value) in enumerate(self._table.items()):
            self._screen.addstr(2 + index, 0, f"{key: <{self._ln}}: {value}")

        last_three = self._last_ptr - 3 if self._last_ptr >= 3 else 0
        self._screen.addnstr(10, 0, ', '.join(self._last_keys[last_three:self._last_ptr]), 50)
        self._screen.addstr(11, 0, f"--> History: {self._last_ptr} / {len(self._last_keys)}")
        self.show_status()

    @on_key("q")
    def quit(self):
        '''quit'''
        return ReturnType.EXIT

    @on_key('1')
    def key_awesome(self):
        """Awesome"""
        key = "Awesome"
        self._push(key)
        return ReturnType.CONTINUE
    
    @on_key('2')
    def key_good(self):
        """Good"""
        key = "Good"
        self._push(key)
        return ReturnType.CONTINUE
    
    @on_key('3')
    def key_normal(self):
        """Normal"""
        key = "Normal"
        self._push(key)
        return ReturnType.CONTINUE
    
    @on_key('4')
    def key_bad(self):
        """Bad"""
        key = "Bad"
        self._push(key)
        return ReturnType.CONTINUE
    
    @on_key('5')
    def key_awful(self):
        """Awful"""
        key = 'Awful'
        self._push(key)
        return ReturnType.CONTINUE
    
    @on_key('u')
    def undo(self):
        """Undo"""
        self._undo()
        return ReturnType.CONTINUE

    @on_key('y')
    def redo(self):
        self._redo()
        return ReturnType.CONTINUE

def init():
    root = Root()
    theme = Theme(0, Basic())
    return root, theme

if __name__ == '__main__':
    run(init)