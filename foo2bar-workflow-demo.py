#
# This was a demo taken from https://github.com/samuell/sciluigi and its
# associated links
#
# Intended for learning purposes only.
#

import sciluigi as sl

class MyWorkflow(sl.WorkflowTask):
    # overrides workflow method
    def workflow(self):
        # init tasks
        foowriter = self.new_task('foowriter', FooWriter)
        foo2bar = self.new_task('foo2bar', Foo2Bar)
        # connect the tasks into a workflow
        foo2bar.in_foo = foowriter.out_foo
        return foo2bar

class FooWriter(sl.Task):
    # out ports - defined as methods
    def out_foo(self):
        return sl.TargetInfo(self, 'foo.txt')
    # defines what the task does
    def run(self):
        with self.out_foo().open('w') as outfile:
            outfile.write('foo\n')

class Foo2Bar(sl.Task):
    in_foo = None
    def out_bar(self):
        return sl.TargetInfo(self, self.in_foo().path + '.bar.txt')
    def run(self):
        self.ex('sed "s/foo/bar/g" {infile} > {outfile}'.format(
        infile=self.in_foo().path,
        outfile=self.out_bar().path))

# main method
if __name__ == '__main__':
    sl.run_local(main_task_cls=MyWorkflow)
