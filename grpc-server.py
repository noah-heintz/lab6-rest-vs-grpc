
from concurrent import futures
import base64
import io
import grpc

from PIL import Image
import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6Servicer):

    def add(self, request, context):
        return lab6_pb2.addReply(
            sum=request.a + request.b
        )

    def dotproduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(
            a * b for a, b in zip(request.a, request.b)
        )

        return lab6_pb2.dotProductReply(
            dotproduct=result
        )

    def rawimage(self, request, context):
        return self.get_image_dimensions(request.img, context)

    def jsonimage(self, request, context):
        try:
            image_bytes = base64.b64decode(
                request.img, validate=True
            )
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid Base64 image data"
            )

        return self.get_image_dimensions(image_bytes, context)

    def get_image_dimensions(self, image_bytes, context):
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                width, height = img.size
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid image data"
            )

        return lab6_pb2.imageReply(
            width=width,
            height=height
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    lab6_pb2_grpc.add_Lab6Servicer_to_server(
        Lab6Service(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC server listening on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
